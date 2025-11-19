-- FUNCTION para obter reservas de um interno USP:
CREATE OR REPLACE FUNCTION get_reservas_interno(cpf_interno VARCHAR)
RETURNS TABLE (
    id_reserva INT,
    nome_instalacao VARCHAR,
    tipo_instalacao VARCHAR,
    data_reserva DATE,
    horario_inicio TIME,
    horario_fim TIME
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        r.id_reserva,
        i.nome AS nome_instalacao,
        i.tipo AS tipo_instalacao,
        r.data_reserva,
        r.horario_inicio,
        r.horario_fim
    FROM reserva r
    JOIN instalacao i
        ON r.id_instalacao = i.id_instalacao
    WHERE r.cpf_responsavel_interno = cpf_interno
    ORDER BY r.data_reserva, r.horario_inicio;
END;
$$ LANGUAGE plpgsql;

-- SELECT * FROM get_reservas_interno('CPF_INTERNO_EXEMPLO');

-- FUNCTION para listar instalações disponíveis em um determinado dia e horário:
CREATE OR REPLACE FUNCTION get_instalacoes_disponiveis_horario(
    dia DATE,
    hora_inicio TIME,
    hora_fim TIME
)
RETURNS TABLE (
    id_instalacao INT,
    nome VARCHAR,
    tipo VARCHAR,
    capacidade INT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        i.id_instalacao,
        i.nome,
        i.tipo,
        i.capacidade
    FROM instalacao i
    WHERE i.eh_reservavel = 'S'
      AND i.id_instalacao NOT IN (
          SELECT r.id_instalacao
          FROM reserva r
          WHERE r.data_reserva = dia
            AND (
                -- verifica se há sobreposição de horários
                (hora_inicio < r.horario_fim AND hora_fim > r.horario_inicio)
            )
      )
    ORDER BY i.nome;
END;
$$ LANGUAGE plpgsql;

-- SELECT * FROM get_instalacoes_disponiveis_horario('2023-11-10', '12:00', '14:00');

-- FUNCTION para listar atividades conduzidas por um educador físico:
CREATE OR REPLACE FUNCTION get_atividades_educador(cpf_educador VARCHAR)
RETURNS TABLE (
    id_atividade INT,
    nome_atividade VARCHAR,
    vagas_limite INT,
    data_inicio DATE,
    data_fim DATE
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id_atividade,
        a.nome AS nome_atividade,
        a.vagas_limite,
        a.data_inicio_periodo AS data_inicio,
        a.data_fim_periodo AS data_fim
    FROM conduz_atividade ca
    JOIN atividade a
        ON a.id_atividade = ca.id_atividade
    WHERE ca.cpf_educador_fisico = cpf_educador
    ORDER BY a.data_inicio_periodo;
END;
$$ LANGUAGE plpgsql;

-- SELECT * FROM get_atividades_educador('CPF_EDUCADOR_EXEMPLO');

-- FUNCTION para calcular total de acessos ao Cefer em um período (reservas + participações):
CREATE OR REPLACE FUNCTION total_acessos_cefer(data_inicio DATE, data_fim DATE)
RETURNS INT AS $$
DECLARE
    total_reservas INT;
    total_participacoes INT;
BEGIN
    -- Contar o número de reservas no período especificado
    SELECT COUNT(DISTINCT r.CPF_RESPONSAVEL_INTERNO)
    INTO total_reservas
    FROM RESERVA r
    JOIN INSTALACAO i ON r.ID_INSTALACAO = i.ID_INSTALACAO
    WHERE r.DATA_RESERVA BETWEEN data_inicio AND data_fim;

    -- Contar o número de participações em atividades no período especificado
    SELECT COUNT(DISTINCT p.CPF_PARTICIPANTE)
    INTO total_participacoes
    FROM PARTICIPACAO_ATIVIDADE p
    JOIN ATIVIDADE a ON p.ID_ATIVIDADE = a.ID_ATIVIDADE
    JOIN OCORRENCIA_SEMANAL o ON a.ID_ATIVIDADE = o.ID_ATIVIDADE
    JOIN INSTALACAO i ON o.ID_INSTALACAO = i.ID_INSTALACAO
    WHERE p.DATA_INSCRICAO BETWEEN data_inicio AND data_fim;

    -- Retornar o total de acessos (reservas + participações)
    RETURN total_reservas + total_participacoes;
END;
$$ LANGUAGE plpgsql;

-- SELECT total_acessos_cefer('2023-07-01', '2023-08-31') AS TOTAL_ACESSOS_CEFER;

-- FUNCTION para listar atividades com filtros opcionais:
CREATE OR REPLACE FUNCTION listar_atividades(
    p_dia_semana DIA_SEMANA DEFAULT NULL,
    p_grupo_extensao VARCHAR(100) DEFAULT NULL,
    p_modalidade VARCHAR(100) DEFAULT NULL
)
RETURNS TABLE (
    id_atividade INT,
    nome_atividade VARCHAR,
    grupo_extensao VARCHAR,
    dia_semana DIA_SEMANA,
    horario_inicio TIME,
    horario_fim TIME,
    vagas_ocupadas INT,
    vagas_limite INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Seleciona atividades com os filtros aplicados
    RETURN QUERY
    SELECT
        a.id_atividade,
        a.nome AS nome_atividade,
        ge.nome_grupo AS grupo_extensao,
        os.dia_semana,
        os.horario_inicio AS horario_inicio,
        os.horario_fim AS horario_fim,
        COUNT(pa.cpf_participante)::integer AS vagas_ocupadas,
        a.vagas_limite
    FROM atividade a
    LEFT JOIN atividade_grupo_extensao ag ON ag.id_atividade = a.id_atividade
    LEFT JOIN grupo_extensao ge ON ge.nome_grupo = ag.nome_grupo
    LEFT JOIN ocorrencia_semanal os ON os.id_atividade = a.id_atividade
    LEFT JOIN participacao_atividade pa ON pa.id_atividade = a.id_atividade
    WHERE
        (p_dia_semana IS NULL OR os.dia_semana = p_dia_semana)
        AND (p_grupo_extensao IS NULL OR ge.nome_grupo ILIKE '%' || p_grupo_extensao || '%')
        AND (p_modalidade IS NULL OR a.nome ILIKE '%' || p_modalidade || '%')
    GROUP BY a.id_atividade, ge.nome_grupo, os.dia_semana, os.horario_inicio, os.horario_fim, a.vagas_limite
    ORDER BY os.dia_semana, os.horario_inicio;
END;
$$;

-- PROCEDURE para cadastrar evento:
CREATE OR REPLACE PROCEDURE cadastrar_evento(
    p_nome VARCHAR,
    p_descricao TEXT,
    p_id_reserva INT
)
AS $$
BEGIN
    INSERT INTO evento (nome, descricao, id_reserva)
    VALUES (p_nome, p_descricao, p_id_reserva);
END;
$$ LANGUAGE plpgsql;


-- PROCEDURE para inscrever participante em atividade com verificação de vagas:
CREATE OR REPLACE PROCEDURE inscrever_participante(
    p_cpf_participante VARCHAR(11),
    p_id_atividade INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verifica se a atividade existe
    IF NOT EXISTS (
        SELECT 1
        FROM atividade
        WHERE id_atividade = p_id_atividade
    ) THEN
        RAISE EXCEPTION 'A atividade com ID % não existe.', p_id_atividade;
    END IF;

    -- Verifica se o participante já está inscrito na atividade
    IF EXISTS (
        SELECT 1
        FROM participacao_atividade
        WHERE cpf_participante = p_cpf_participante
        AND id_atividade = p_id_atividade
    ) THEN
        RAISE NOTICE 'O participante já está inscrito nesta atividade.';
        RETURN;
    END IF;

    -- Verifica se há vagas disponíveis para a atividade
    IF EXISTS (
        SELECT 1
        FROM atividade a
        LEFT JOIN participacao_atividade pa ON pa.id_atividade = a.id_atividade
        WHERE a.id_atividade = p_id_atividade
        GROUP BY a.vagas_limite
        HAVING COUNT(pa.cpf_participante) >= a.vagas_limite
    ) THEN
        RAISE EXCEPTION 'A atividade com ID % já está com as vagas esgotadas.', p_id_atividade;
    END IF;

    -- Inscreve o participante na atividade
    INSERT INTO participacao_atividade (cpf_participante, id_atividade, data_inscricao)
    VALUES (p_cpf_participante, p_id_atividade, CURRENT_DATE);

    RAISE NOTICE 'Inscrição realizada com sucesso para a atividade com ID %.', p_id_atividade;
END;
$$;
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

