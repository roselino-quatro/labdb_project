-- Enable pgcrypto extension for password hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- FUNCTION: hash_password
-- Generates bcrypt hash for a plain password
-- Parameters:
--   plain_password: The plain text password to hash
-- Returns: Hashed password string
CREATE OR REPLACE FUNCTION hash_password(plain_password TEXT)
RETURNS TEXT
AS $$
BEGIN
    RETURN crypt(plain_password, gen_salt('bf', 10));
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: verify_password
-- Verifies if a plain password matches the hashed password
-- Parameters:
--   plain_password: The plain text password to verify
--   hashed_password: The stored hash to compare against
-- Returns: TRUE if password matches, FALSE otherwise
CREATE OR REPLACE FUNCTION verify_password(plain_password TEXT, hashed_password TEXT)
RETURNS BOOLEAN
AS $$
BEGIN
    RETURN hashed_password = crypt(plain_password, hashed_password);
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: get_user_roles
-- Determines user roles based on database relationships
-- Parameters:
--   cpf_pessoa: CPF of the user
-- Returns: JSON object with roles array
CREATE OR REPLACE FUNCTION get_user_roles(cpf_pessoa VARCHAR)
RETURNS JSON
AS $$
DECLARE
    roles JSON;
    is_admin BOOLEAN := FALSE;
    is_staff BOOLEAN := FALSE;
    is_internal BOOLEAN := FALSE;
    is_external BOOLEAN := FALSE;
    roles_array TEXT[] := ARRAY[]::TEXT[];
BEGIN
    -- Check if user is admin (has 'Administrador' in FUNCIONARIO_ATRIBUICAO)
    SELECT EXISTS(
        SELECT 1
        FROM funcionario_atribuicao fa
        JOIN funcionario f ON fa.cpf_funcionario = f.cpf_interno
        WHERE f.cpf_interno = cpf_pessoa
        AND fa.atribuicao LIKE '%Administrador%'
    ) INTO is_admin;

    -- Check if user is staff (exists in FUNCIONARIO)
    SELECT EXISTS(
        SELECT 1
        FROM funcionario
        WHERE cpf_interno = cpf_pessoa
    ) INTO is_staff;

    -- Check if user is internal (exists in INTERNO_USP)
    SELECT EXISTS(
        SELECT 1
        FROM interno_usp
        WHERE interno_usp.cpf_pessoa = get_user_roles.cpf_pessoa
    ) INTO is_internal;

    -- Check if user is external (exists in PESSOA but not in INTERNO_USP and has CONVITE_EXTERNO)
    SELECT EXISTS(
        SELECT 1
        FROM pessoa p
        WHERE p.cpf = cpf_pessoa
        AND NOT EXISTS (
            SELECT 1 FROM interno_usp i WHERE i.cpf_pessoa = p.cpf
        )
        AND EXISTS (
            SELECT 1 FROM convite_externo ce WHERE ce.email_convidado = p.email
        )
    ) INTO is_external;

    -- Build roles array
    IF is_admin THEN
        roles_array := array_append(roles_array, 'admin');
    END IF;
    IF is_staff THEN
        roles_array := array_append(roles_array, 'staff');
    END IF;
    IF is_internal THEN
        roles_array := array_append(roles_array, 'internal');
    END IF;
    IF is_external THEN
        roles_array := array_append(roles_array, 'external');
    END IF;

    -- Return as JSON
    roles := json_build_object('roles', roles_array);
    RETURN roles;
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: request_registration
-- Creates a registration request for an internal USP user
-- Parameters:
--   cpf_pessoa: CPF of the person
--   nusp: NUSP number
--   email: Email address
--   plain_password: Plain text password (will be stored in solicitation, hashed on approval)
-- Returns: JSON with success status and message
CREATE OR REPLACE FUNCTION request_registration(
    cpf_pessoa VARCHAR,
    nusp VARCHAR,
    email VARCHAR,
    plain_password TEXT
)
RETURNS JSON
AS $$
DECLARE
    result JSON;
    pessoa_exists BOOLEAN;
    interno_exists BOOLEAN;
    nusp_matches BOOLEAN;
    request_exists BOOLEAN;
    email_matches BOOLEAN;
BEGIN
    -- Check if person exists
    SELECT EXISTS(SELECT 1 FROM pessoa WHERE cpf = cpf_pessoa) INTO pessoa_exists;
    IF NOT pessoa_exists THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'CPF not found in database'
        );
    END IF;

    -- Check if email matches
    SELECT EXISTS(SELECT 1 FROM pessoa WHERE cpf = cpf_pessoa AND email = request_registration.email) INTO email_matches;
    IF NOT email_matches THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Email does not match CPF'
        );
    END IF;

    -- Check if person is internal USP
    SELECT EXISTS(SELECT 1 FROM interno_usp WHERE cpf_pessoa = request_registration.cpf_pessoa) INTO interno_exists;
    IF NOT interno_exists THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Only internal USP members can request registration'
        );
    END IF;

    -- Check if NUSP matches
    SELECT EXISTS(SELECT 1 FROM interno_usp WHERE cpf_pessoa = request_registration.cpf_pessoa AND nusp = request_registration.nusp) INTO nusp_matches;
    IF NOT nusp_matches THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'NUSP does not match CPF'
        );
    END IF;

    -- Check if request already exists
    SELECT EXISTS(
        SELECT 1 FROM solicitacao_cadastro
        WHERE cpf_pessoa = request_registration.cpf_pessoa
        AND status = 'PENDENTE'
    ) INTO request_exists;
    IF request_exists THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Registration request already pending'
        );
    END IF;

    -- Check if user already has account
    IF EXISTS(SELECT 1 FROM usuario_senha WHERE cpf_pessoa = request_registration.cpf_pessoa) THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'User already has an account'
        );
    END IF;

    -- Create registration request (store plain password temporarily, will be hashed on approval)
    INSERT INTO solicitacao_cadastro (cpf_pessoa, nusp, status, observacoes)
    VALUES (cpf_pessoa, nusp, 'PENDENTE', 'Password: ' || plain_password);

    RETURN json_build_object(
        'success', TRUE,
        'message', 'Registration request created successfully. Awaiting admin approval.'
    );
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: approve_registration
-- Approves a registration request and creates user account with hashed password
-- Parameters:
--   id_solicitacao: ID of the registration request
--   cpf_admin: CPF of the admin approving the request
-- Returns: JSON with success status and message
CREATE OR REPLACE FUNCTION approve_registration(
    id_solicitacao INT,
    cpf_admin VARCHAR
)
RETURNS JSON
AS $$
DECLARE
    solicitation_record RECORD;
    password_hash TEXT;
    plain_password TEXT;
BEGIN
    -- Get solicitation record
    SELECT * INTO solicitation_record
    FROM solicitacao_cadastro
    WHERE id_solicitacao = approve_registration.id_solicitacao;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Registration request not found'
        );
    END IF;

    IF solicitation_record.status != 'PENDENTE' THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Registration request is not pending'
        );
    END IF;

    -- Extract plain password from observacoes (temporary storage)
    plain_password := substring(solicitation_record.observacoes FROM 'Password: (.+)');

    -- Hash the password
    password_hash := hash_password(plain_password);

    -- Create user account
    INSERT INTO usuario_senha (cpf_pessoa, senha_hash, data_criacao)
    VALUES (solicitation_record.cpf_pessoa, password_hash, CURRENT_TIMESTAMP)
    ON CONFLICT (cpf_pessoa) DO UPDATE
    SET senha_hash = EXCLUDED.senha_hash,
        data_ultima_alteracao = CURRENT_TIMESTAMP;

    -- Update solicitation status
    UPDATE solicitacao_cadastro
    SET status = 'APROVADA',
        cpf_admin_aprovador = cpf_admin,
        data_aprovacao = CURRENT_TIMESTAMP,
        observacoes = NULL  -- Remove password from observacoes
    WHERE id_solicitacao = approve_registration.id_solicitacao;

    RETURN json_build_object(
        'success', TRUE,
        'message', 'Registration approved and user account created'
    );
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: reject_registration
-- Rejects a registration request
-- Parameters:
--   id_solicitacao: ID of the registration request
--   cpf_admin: CPF of the admin rejecting the request
--   observacoes: Optional rejection reason
-- Returns: JSON with success status and message
CREATE OR REPLACE FUNCTION reject_registration(
    id_solicitacao INT,
    cpf_admin VARCHAR,
    observacoes TEXT DEFAULT NULL
)
RETURNS JSON
AS $$
DECLARE
    solicitation_record RECORD;
BEGIN
    -- Get solicitation record
    SELECT * INTO solicitation_record
    FROM solicitacao_cadastro
    WHERE id_solicitacao = reject_registration.id_solicitacao;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Registration request not found'
        );
    END IF;

    IF solicitation_record.status != 'PENDENTE' THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Registration request is not pending'
        );
    END IF;

    -- Update solicitation status
    UPDATE solicitacao_cadastro
    SET status = 'REJEITADA',
        cpf_admin_aprovador = cpf_admin,
        data_aprovacao = CURRENT_TIMESTAMP,
        observacoes = reject_registration.observacoes
    WHERE id_solicitacao = reject_registration.id_solicitacao;

    RETURN json_build_object(
        'success', TRUE,
        'message', 'Registration request rejected'
    );
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: authenticate_user
-- Authenticates a user and returns their roles
-- Parameters:
--   email_or_cpf: Email or CPF of the user
--   plain_password: Plain text password
--   ip_origin: IP address of the login attempt
-- Returns: JSON with success status, user data, and roles
CREATE OR REPLACE FUNCTION authenticate_user(
    email_or_cpf VARCHAR,
    plain_password TEXT,
    ip_origin VARCHAR DEFAULT NULL
)
RETURNS JSON
AS $$
DECLARE
    user_record RECORD;
    password_record RECORD;
    password_valid BOOLEAN;
    roles_json JSON;
    result JSON;
BEGIN
    -- Find user by email or CPF
    SELECT * INTO user_record
    FROM pessoa
    WHERE email = email_or_cpf OR cpf = email_or_cpf;

    IF NOT FOUND THEN
        -- Log failed attempt
        INSERT INTO auditoria_login (email_usuario, ip_origem, status, mensagem)
        VALUES (email_or_cpf, ip_origin, 'FAILURE', 'User not found');

        RETURN json_build_object(
            'success', FALSE,
            'message', 'Invalid credentials'
        );
    END IF;

    -- Get password record
    SELECT * INTO password_record
    FROM usuario_senha
    WHERE cpf_pessoa = user_record.cpf;

    IF NOT FOUND THEN
        -- Log failed attempt
        INSERT INTO auditoria_login (email_usuario, ip_origem, status, mensagem)
        VALUES (user_record.email, ip_origin, 'FAILURE', 'User account not found');

        RETURN json_build_object(
            'success', FALSE,
            'message', 'Invalid credentials'
        );
    END IF;

    -- Check if account is blocked
    IF password_record.bloqueado THEN
        INSERT INTO auditoria_login (email_usuario, ip_origem, status, mensagem)
        VALUES (user_record.email, ip_origin, 'LOCKED', 'Account is blocked');

        RETURN json_build_object(
            'success', FALSE,
            'message', 'Account is blocked'
        );
    END IF;

    -- Verify password
    password_valid := verify_password(plain_password, password_record.senha_hash);

    IF NOT password_valid THEN
        -- Increment failed attempts
        UPDATE usuario_senha
        SET tentativas_login = tentativas_login + 1
        WHERE cpf_pessoa = user_record.cpf;

        -- Block account after 5 failed attempts
        IF password_record.tentativas_login + 1 >= 5 THEN
            UPDATE usuario_senha
            SET bloqueado = TRUE
            WHERE cpf_pessoa = user_record.cpf;
        END IF;

        -- Log failed attempt
        INSERT INTO auditoria_login (email_usuario, ip_origem, status, mensagem)
        VALUES (user_record.email, ip_origin, 'FAILURE', 'Invalid password');

        RETURN json_build_object(
            'success', FALSE,
            'message', 'Invalid credentials'
        );
    END IF;

    -- Reset failed attempts and update last login
    UPDATE usuario_senha
    SET tentativas_login = 0,
        data_ultimo_login = CURRENT_TIMESTAMP
    WHERE cpf_pessoa = user_record.cpf;

    -- Get user roles
    roles_json := get_user_roles(user_record.cpf);

    -- Log successful login
    INSERT INTO auditoria_login (email_usuario, ip_origem, status, mensagem)
    VALUES (user_record.email, ip_origin, 'SUCCESS', 'Login successful');

    -- Build result
    result := json_build_object(
        'success', TRUE,
        'user_id', user_record.cpf,
        'email', user_record.email,
        'nome', user_record.nome,
        'roles', roles_json->'roles'
    );

    RETURN result;
END;
$$ LANGUAGE plpgsql;
