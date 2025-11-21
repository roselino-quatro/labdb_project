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
    SELECT EXISTS(SELECT 1 FROM pessoa p WHERE p.cpf = request_registration.cpf_pessoa) INTO pessoa_exists;
    IF NOT pessoa_exists THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'CPF not found in database'
        );
    END IF;

    -- Check if email matches
    SELECT EXISTS(SELECT 1 FROM pessoa p WHERE p.cpf = request_registration.cpf_pessoa AND p.email = request_registration.email) INTO email_matches;
    IF NOT email_matches THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Email does not match CPF'
        );
    END IF;

    -- Check if person is internal USP
    SELECT EXISTS(SELECT 1 FROM interno_usp i WHERE i.cpf_pessoa = request_registration.cpf_pessoa) INTO interno_exists;
    IF NOT interno_exists THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Only internal USP members can request registration'
        );
    END IF;

    -- Check if NUSP matches
    SELECT EXISTS(SELECT 1 FROM interno_usp i WHERE i.cpf_pessoa = request_registration.cpf_pessoa AND i.nusp = request_registration.nusp) INTO nusp_matches;
    IF NOT nusp_matches THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'NUSP does not match CPF'
        );
    END IF;

    -- Check if request already exists
    SELECT EXISTS(
        SELECT 1 FROM solicitacao_cadastro sc
        WHERE sc.cpf_pessoa = request_registration.cpf_pessoa
        AND sc.status = 'PENDENTE'
    ) INTO request_exists;
    IF request_exists THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Registration request already pending'
        );
    END IF;

    -- Check if user already has account
    IF EXISTS(SELECT 1 FROM usuario_senha us WHERE us.cpf_pessoa = request_registration.cpf_pessoa) THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'User already has an account'
        );
    END IF;

    -- Create registration request (store plain password temporarily, will be hashed on approval)
    INSERT INTO solicitacao_cadastro (cpf_pessoa, nusp, status, observacoes)
    VALUES (request_registration.cpf_pessoa, request_registration.nusp, 'PENDENTE', 'Password: ' || request_registration.plain_password);

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

-- FUNCTION: authenticate_external_by_token
-- Authenticates an external user by token and returns invite information
-- Parameters:
--   token: The invite token
-- Returns: JSON with success status, invite data, and activity information
CREATE OR REPLACE FUNCTION authenticate_external_by_token(token VARCHAR)
RETURNS JSON
AS $$
DECLARE
    invite_record RECORD;
    activity_record RECORD;
    result JSON;
BEGIN
    -- Find invite by token
    SELECT * INTO invite_record
    FROM convite_externo
    WHERE convite_externo.token = authenticate_external_by_token.token;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Token inválido ou convite não encontrado'
        );
    END IF;

    -- Check if invite status is valid (PENDENTE or ACEITO)
    IF invite_record.status NOT IN ('PENDENTE', 'ACEITO') THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Convite não está disponível. Status: ' || invite_record.status
        );
    END IF;

    -- Get activity information if exists
    IF invite_record.id_atividade IS NOT NULL THEN
        SELECT * INTO activity_record
        FROM atividade
        WHERE id_atividade = invite_record.id_atividade;
    END IF;

    -- Build result with invite and activity data
    result := json_build_object(
        'success', TRUE,
        'invite_id', invite_record.id_convite,
        'invite_status', invite_record.status,
        'invite_data', json_build_object(
            'nome_convidado', invite_record.nome_convidado,
            'documento_convidado', invite_record.documento_convidado,
            'email_convidado', invite_record.email_convidado,
            'telefone_convidado', invite_record.telefone_convidado,
            'data_convite', invite_record.data_convite,
            'data_resposta', invite_record.data_resposta,
            'observacoes', invite_record.observacoes
        ),
        'activity_id', invite_record.id_atividade,
        'activity_data', CASE
            WHEN activity_record.id_atividade IS NOT NULL THEN
                json_build_object(
                    'id_atividade', activity_record.id_atividade,
                    'nome', activity_record.nome,
                    'vagas_limite', activity_record.vagas_limite,
                    'data_inicio_periodo', activity_record.data_inicio_periodo,
                    'data_fim_periodo', activity_record.data_fim_periodo
                )
            ELSE NULL
        END
    );

    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: accept_external_invite
-- Accepts an external invite and creates participation if document is valid CPF
-- Parameters:
--   invite_id: ID of the invite
-- Returns: JSON with success status and message
CREATE OR REPLACE FUNCTION accept_external_invite(invite_id INT)
RETURNS JSON
AS $$
DECLARE
    invite_record RECORD;
    activity_record RECORD;
    pessoa_exists BOOLEAN;
    participation_exists BOOLEAN;
    is_valid_cpf BOOLEAN;
    current_participants_count INT;
    cpf_document VARCHAR(11);
BEGIN
    -- Get invite record
    SELECT * INTO invite_record
    FROM convite_externo
    WHERE id_convite = accept_external_invite.invite_id;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Convite não encontrado'
        );
    END IF;

    IF invite_record.status != 'PENDENTE' THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Convite não está pendente. Status atual: ' || invite_record.status
        );
    END IF;

    -- Check if DOCUMENTO_CONVIDADO is a valid CPF (11 digits, numeric only)
    is_valid_cpf := LENGTH(TRIM(invite_record.documento_convidado)) = 11
                    AND invite_record.documento_convidado ~ '^[0-9]+$';

    -- If document is a valid CPF, create PESSOA and PARTICIPACAO_ATIVIDADE
    IF is_valid_cpf THEN
        cpf_document := TRIM(invite_record.documento_convidado);

        -- Check if PESSOA already exists
        SELECT EXISTS(SELECT 1 FROM pessoa WHERE cpf = cpf_document) INTO pessoa_exists;

        -- Create or update PESSOA record
        -- Note: PESSOA.email is NOT NULL, so we use a default email if not provided
        IF NOT pessoa_exists THEN
            INSERT INTO pessoa (cpf, nome, email, celular)
            VALUES (
                cpf_document,
                invite_record.nome_convidado,
                COALESCE(invite_record.email_convidado, cpf_document || '@externo.cefer.usp.br'),
                invite_record.telefone_convidado
            )
            ON CONFLICT (cpf) DO UPDATE
            SET nome = EXCLUDED.nome,
                email = CASE
                    WHEN EXCLUDED.email IS NOT NULL AND EXCLUDED.email != '' THEN EXCLUDED.email
                    ELSE pessoa.email
                END,
                celular = COALESCE(EXCLUDED.celular, pessoa.celular);
        ELSE
            -- Update existing PESSOA if needed
            UPDATE pessoa
            SET nome = invite_record.nome_convidado,
                email = CASE
                    WHEN invite_record.email_convidado IS NOT NULL AND invite_record.email_convidado != ''
                    THEN invite_record.email_convidado
                    ELSE pessoa.email
                END,
                celular = COALESCE(invite_record.telefone_convidado, pessoa.celular)
            WHERE cpf = cpf_document;
        END IF;

        -- Check if activity exists and get its information
        IF invite_record.id_atividade IS NOT NULL THEN
            SELECT * INTO activity_record
            FROM atividade
            WHERE id_atividade = invite_record.id_atividade;

            IF FOUND THEN
                -- Check if participant is already registered
                SELECT EXISTS(
                    SELECT 1
                    FROM participacao_atividade
                    WHERE cpf_participante = cpf_document
                    AND id_atividade = invite_record.id_atividade
                ) INTO participation_exists;

                IF NOT participation_exists THEN
                    -- Check if there are available spots
                    SELECT COUNT(*) INTO current_participants_count
                    FROM participacao_atividade
                    WHERE id_atividade = invite_record.id_atividade;

                    -- If activity has a limit and it's reached, don't create participation
                    IF activity_record.vagas_limite IS NOT NULL
                       AND current_participants_count >= activity_record.vagas_limite THEN
                        -- Update invite status to ACEITO but don't create participation
                        UPDATE convite_externo
                        SET status = 'ACEITO',
                            data_resposta = CURRENT_TIMESTAMP
                        WHERE id_convite = accept_external_invite.invite_id;

                        RETURN json_build_object(
                            'success', TRUE,
                            'message', 'Convite aceito, mas a atividade está com vagas esgotadas. Entre em contato com o organizador.'
                        );
                    END IF;

                    -- Create participation record
                    INSERT INTO participacao_atividade (
                        cpf_participante,
                        id_atividade,
                        cpf_convidante_interno,
                        data_inscricao
                    )
                    VALUES (
                        cpf_document,
                        invite_record.id_atividade,
                        invite_record.cpf_convidante,
                        CURRENT_DATE
                    );
                END IF;
            END IF;
        END IF;
    END IF;

    -- Update invite status
    UPDATE convite_externo
    SET status = 'ACEITO',
        data_resposta = CURRENT_TIMESTAMP
    WHERE id_convite = accept_external_invite.invite_id;

    RETURN json_build_object(
        'success', TRUE,
        'message', CASE
            WHEN is_valid_cpf AND invite_record.id_atividade IS NOT NULL THEN
                'Convite aceito e participação criada com sucesso'
            WHEN is_valid_cpf THEN
                'Convite aceito. PESSOA criada/atualizada.'
            ELSE
                'Convite aceito com sucesso'
        END
    );
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: reject_external_invite
-- Rejects an external invite
-- Parameters:
--   invite_id: ID of the invite
-- Returns: JSON with success status and message
CREATE OR REPLACE FUNCTION reject_external_invite(invite_id INT)
RETURNS JSON
AS $$
DECLARE
    invite_record RECORD;
BEGIN
    -- Get invite record
    SELECT * INTO invite_record
    FROM convite_externo
    WHERE id_convite = reject_external_invite.invite_id;

    IF NOT FOUND THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Convite não encontrado'
        );
    END IF;

    IF invite_record.status != 'PENDENTE' THEN
        RETURN json_build_object(
            'success', FALSE,
            'message', 'Convite não está pendente. Status atual: ' || invite_record.status
        );
    END IF;

    -- Update invite status
    UPDATE convite_externo
    SET status = 'RECUSADO',
        data_resposta = CURRENT_TIMESTAMP
    WHERE id_convite = reject_external_invite.invite_id;

    RETURN json_build_object(
        'success', TRUE,
        'message', 'Convite recusado'
    );
END;
$$ LANGUAGE plpgsql;
