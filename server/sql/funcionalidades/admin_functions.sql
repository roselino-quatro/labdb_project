-- PESSOA
-- CREATE
CREATE OR REPLACE PROCEDURE criar_pessoa(
    p_cpf VARCHAR,
    p_nome VARCHAR,
    p_email VARCHAR,
    p_celular VARCHAR,
    p_data_nascimento DATE
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO PESSOA (CPF, NOME, EMAIL, CELULAR, DATA_NASCIMENTO)
    VALUES (p_cpf, p_nome, p_email, p_celular, p_data_nascimento);
END;
$$;

-- READ
CREATE OR REPLACE FUNCTION listar_pessoas()
RETURNS TABLE(cpf VARCHAR, nome VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT P.CPF, P.NOME, P.EMAIL FROM PESSOA P;
END;
$$ LANGUAGE plpgsql;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_pessoa(
    p_cpf VARCHAR,
    p_nome_novo VARCHAR,
    p_email_novo VARCHAR,
    p_celular_novo VARCHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE pessoa SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_nome_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' nome = ''' || p_nome_novo || ''',';
    END IF;
    IF p_email_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' email = ''' || p_email_novo || ''',';
    END IF;
    IF p_celular_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' celular = ''' || p_celular_novo || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE cpf = ''' || p_cpf || '''';

    EXECUTE v_cmd;
    
    IF NOT FOUND THEN RAISE EXCEPTION 'Pessoa com CPF % não encontrada.', p_cpf; END IF;
END;
$$;

-- DELETE
CREATE OR REPLACE PROCEDURE deletar_pessoa(p_cpf VARCHAR) 
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM PESSOA WHERE CPF = p_cpf;
    IF NOT FOUND THEN RAISE EXCEPTION 'Pessoa não encontrada.'; END IF;
END;
$$;

-- INTERNO_USP
-- CREATE
CREATE OR REPLACE PROCEDURE criar_interno(
    -- Dados Pessoais
    p_cpf VARCHAR,
    p_nome VARCHAR,
    p_email VARCHAR,
    p_celular VARCHAR,
    p_data_nascimento DATE,
    -- Dados de Interno
    p_nusp VARCHAR,
    p_categoria VARCHAR
) LANGUAGE plpgsql AS $$
BEGIN
    CALL criar_pessoa(p_cpf, p_nome, p_email, p_celular, p_data_nascimento);

    INSERT INTO INTERNO_USP (CPF_PESSOA, NUSP, CATEGORIA)
    VALUES (p_cpf, p_nusp, p_categoria);
END;
$$;

-- READ
CREATE OR REPLACE FUNCTION listar_internos()
RETURNS TABLE(cpf VARCHAR, nome VARCHAR, nusp VARCHAR, categoria VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT P.CPF, P.NOME, I.NUSP, I.CATEGORIA
    FROM PESSOA P
    INNER JOIN INTERNO_USP I ON P.CPF = I.CPF_PESSOA;
END;
$$ LANGUAGE plpgsql;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_interno(
    p_cpf VARCHAR,
    p_categoria_nova VARCHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE interno_usp SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_categoria_nova IS NOT NULL THEN
      v_cmd := v_cmd || ' categoria = ''' || p_categoria_nova || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE cpf = ''' || p_cpf || '''';

    EXECUTE v_cmd;
    
    IF NOT FOUND THEN RAISE EXCEPTION 'Interno não encontrado.'; END IF;
END;
$$;


-- FUNCIONÁRIO
-- CREATE
CREATE OR REPLACE PROCEDURE criar_funcionario(
    -- Dados Pessoais
    p_cpf VARCHAR,
    p_nome VARCHAR,
    p_email VARCHAR,
    p_celular VARCHAR,
    p_data_nascimento DATE,
    -- Dados de Interno
    p_nusp VARCHAR,
    -- Dados de Funcionário
    p_formacao VARCHAR
) LANGUAGE plpgsql AS $$
BEGIN
    CALL criar_interno(p_cpf, p_nome, p_email, p_celular, p_data_nascimento, p_nusp, 'FUNCIONARIO');

    INSERT INTO FUNCIONARIO (CPF_INTERNO, FORMACAO)
    VALUES (p_cpf, p_formacao);
END;
$$;

-- READ
CREATE OR REPLACE FUNCTION listar_funcionarios()
RETURNS TABLE(cpf VARCHAR, nome VARCHAR, nusp VARCHAR, formacao VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT P.CPF, P.NOME, I.NUSP, F.FORMACAO
    FROM PESSOA P
    INNER JOIN INTERNO_USP I ON P.CPF = I.CPF_PESSOA
    INNER JOIN FUNCIONARIO F ON I.CPF_PESSOA = F.CPF_INTERNO;
END;
$$ LANGUAGE plpgsql;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_funcionario(
    p_cpf VARCHAR,
    p_formacao_nova VARCHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE funcionario SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_formacao_nova IS NOT NULL THEN
      v_cmd := v_cmd || ' formacao = ''' || p_formacao_nova || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE cpf = ''' || p_cpf || '''';

    EXECUTE v_cmd;
    
    IF NOT FOUND THEN RAISE EXCEPTION 'Funcionário não encontrado.'; END IF;
END;
$$;

-- EDUCADOR FÍSICO
-- CREATE
CREATE OR REPLACE PROCEDURE criar_educador_fisico(
    -- Dados Pessoais
    p_cpf VARCHAR,
    p_nome VARCHAR,
    p_email VARCHAR,
    p_celular VARCHAR,
    p_data_nascimento DATE,
    -- Dados de Interno
    p_nusp VARCHAR,
    -- Dados de Funcionário
    p_formacao VARCHAR,
    -- Dados de Educador
    p_numero_conselho VARCHAR
) LANGUAGE plpgsql AS $$
BEGIN
    CALL criar_funcionario(p_cpf, p_nome, p_email, p_celular, p_data_nascimento, p_nusp, p_formacao);

    INSERT INTO EDUCADOR_FISICO (CPF_FUNCIONARIO, NUMERO_CONSELHO)
    VALUES (p_cpf, p_numero_conselho);
END;
$$;

-- READ
CREATE OR REPLACE FUNCTION listar_educadores()
RETURNS TABLE(cpf VARCHAR, nome VARCHAR, nusp VARCHAR, conselho VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT P.CPF, P.NOME, I.NUSP, E.NUMERO_CONSELHO
    FROM PESSOA P
    INNER JOIN INTERNO_USP I ON P.CPF = I.CPF_PESSOA
    INNER JOIN FUNCIONARIO F ON I.CPF_PESSOA = F.CPF_INTERNO
    INNER JOIN EDUCADOR_FISICO E ON F.CPF_INTERNO = E.CPF_FUNCIONARIO;
END;
$$ LANGUAGE plpgsql;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_educador(
    p_cpf VARCHAR,
    p_conselho_novo VARCHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE educador_fisico SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_conselho_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' numero_conselho = ''' || p_conselho_novo || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE cpf = ''' || p_cpf || '''';

    EXECUTE v_cmd;

    IF NOT FOUND THEN RAISE EXCEPTION 'Educador físico não encontrado.'; END IF;
END;
$$;

-- Grupos de extensão
-- CREATE 
CREATE OR REPLACE PROCEDURE criar_grupo_extensao(
    p_nome VARCHAR,
    p_descricao TEXT,
    p_cpf_responsavel VARCHAR
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO GRUPO_EXTENSAO (NOME_GRUPO, DESCRICAO, CPF_RESPONSAVEL_INTERNO)
    VALUES (p_nome, p_descricao, p_cpf_responsavel);
END;
$$;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_grupo_extensao(
    p_nome_antigo VARCHAR,
    p_nome_novo VARCHAR,
    p_descricao_nova TEXT,
    p_cpf_responsavel_novo VARCHAR 
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE grupo_extensao SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_nome_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' nome_grupo = ''' || p_nome_novo || ''',';
    END IF;
    IF p_descricao_nova IS NOT NULL THEN
      v_cmd := v_cmd || ' descricao = ''' || p_descricao_nova || ''',';
    END IF;
    IF p_cpf_responsavel_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' cpf_responsavel_interno = ''' || p_cpf_responsavel_novo || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE nome_grupo = ''' || p_nome_antigo || '''';

    EXECUTE v_cmd;
END;
$$;

-- DELETE
CREATE OR REPLACE PROCEDURE deletar_grupo_extensao(p_nome VARCHAR) 
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM GRUPO_EXTENSAO WHERE NOME_GRUPO = p_nome;
END;
$$;

-- Equipamento
-- CREATE
CREATE OR REPLACE PROCEDURE criar_equipamento(
    p_id_patrimonio VARCHAR,
    p_nome VARCHAR,
    p_id_instalacao INT,
    p_preco DECIMAL,
    p_data_aquisicao DATE,
    p_eh_reservavel CHAR
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO EQUIPAMENTO (ID_PATRIMONIO, NOME, ID_INSTALACAO_LOCAL, PRECO_AQUISICAO, DATA_AQUISICAO, EH_RESERVAVEL)
    VALUES (p_id_patrimonio, p_nome, p_id_instalacao, p_preco, p_data_aquisicao, p_eh_reservavel);
END;
$$;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_equipamento(
    p_id_patrimonio VARCHAR,
    p_nome_novo VARCHAR,
    p_id_instalacao_novo INT,
    p_eh_reservavel_novo CHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE equipamento SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_nome IS NOT NULL THEN
      v_cmd := v_cmd || ' nome = ''' || p_nome_novo || ''',';
    END IF;
    IF p_id_instalacao IS NOT NULL THEN
      v_cmd := v_cmd || ' id_instalacao_local = ''' || p_id_instalacao_novo || ''',';
    END IF;
    IF p_cpf_responsavel_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' eh_reservavel = ''' || p_eh_reservavel_novo || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE id_patrimonio = ''' || p_id_patrimonio || '''';

    EXECUTE v_cmd;
    
    IF NOT FOUND THEN RAISE EXCEPTION 'Equipamento não encontrado.'; END IF;
END;
$$;

-- DELETE
CREATE OR REPLACE PROCEDURE deletar_equipamento(p_id VARCHAR) 
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM EQUIPAMENTO WHERE ID_PATRIMONIO = p_id;
    IF NOT FOUND THEN RAISE EXCEPTION 'Equipamento não encontrado.'; END IF;
END;
$$;

-- Instalação
-- CREATE
CREATE OR REPLACE PROCEDURE criar_instalacao(
    p_nome VARCHAR,
    p_tipo VARCHAR,
    p_capacidade INT,
    p_eh_reservavel CHAR
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO INSTALACAO (NOME, TIPO, CAPACIDADE, EH_RESERVAVEL)
    VALUES (p_nome, p_tipo, p_capacidade, p_eh_reservavel);
END;
$$;

-- READ
CREATE OR REPLACE FUNCTION listar_instalacoes()
RETURNS TABLE(id INT, nome VARCHAR, tipo VARCHAR, capacidade INT, reservavel CHAR) AS $$
BEGIN
    RETURN QUERY SELECT ID_INSTALACAO, NOME, TIPO, CAPACIDADE, EH_RESERVAVEL FROM INSTALACAO;
END;
$$ LANGUAGE plpgsql;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_instalacao(
    p_id INT,
    p_nome_novo VARCHAR,
    p_capacidade_novo INT,
    p_eh_reservavel_novo CHAR
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE instalacao SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_nome IS NOT NULL THEN
      v_cmd := v_cmd || ' nome = ''' || p_nome_novo || ''',';
    END IF;
    IF p_capacidade IS NOT NULL THEN
      v_cmd := v_cmd || ' capacidade = ''' || p_capacidade_novo || ''',';
    END IF;
    IF p_eh_reservavel IS NOT NULL THEN
      v_cmd := v_cmd || ' eh_reservavel = ''' || p_eh_reservavel_novo || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE id_instalacao = ''' || p_id || '''';

    EXECUTE v_cmd;
    
    IF NOT FOUND THEN RAISE EXCEPTION 'Instalação não encontrada.'; END IF;
END;
$$;

-- DELETE
CREATE OR REPLACE PROCEDURE deletar_instalacao(p_id INT) 
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM INSTALACAO WHERE ID_INSTALACAO = p_id;
    IF NOT FOUND THEN RAISE EXCEPTION 'Instalação não encontrada.'; END IF;
END;
$$;

-- Evento
-- CREATE
CREATE OR REPLACE PROCEDURE criar_evento(
    p_nome VARCHAR,
    p_descricao TEXT,
    p_id_reserva INT
) LANGUAGE plpgsql AS $$
BEGIN
    -- Verifica se a reserva existe
    IF NOT EXISTS (SELECT 1 FROM RESERVA WHERE ID_RESERVA = p_id_reserva) THEN
        RAISE EXCEPTION 'Reserva % não encontrada. Crie a reserva antes do evento.', p_id_reserva;
    END IF;

    INSERT INTO EVENTO (NOME, DESCRICAO, ID_RESERVA)
    VALUES (p_nome, p_descricao, p_id_reserva);
END;
$$;

-- UPDATE
CREATE OR REPLACE PROCEDURE atualizar_evento(
    p_id_evento INT,
    p_nome_novo VARCHAR,
    p_descricao_nova TEXT
) LANGUAGE plpgsql AS $$
DECLARE
    v_cmd TEXT;
BEGIN
    v_cmd := 'UPDATE evento SET ';
    -- Lógica para adicionar os updates baseado se um valor NULL foi passado
    IF p_nome_novo IS NOT NULL THEN
      v_cmd := v_cmd || ' nome = ''' || p_nome_novo || ''',';
    END IF;
    IF p_descricao_nova IS NOT NULL THEN
      v_cmd := v_cmd || ' descricao = ''' || p_descricao_nova || ''',';
    END IF;

    -- Corta o ultimo caracter, que seria uma virgula de um dos SETs
    v_cmd := left(v_cmd, -1);
    v_cmd := v_cmd || ' WHERE id_evento = ''' || p_id_evento || '''';

    EXECUTE v_cmd;

    IF NOT FOUND THEN RAISE EXCEPTION 'Evento não encontrado.'; END IF;
END;
$$;

-- DELETE
CREATE OR REPLACE PROCEDURE deletar_evento(p_id_evento INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM EVENTO WHERE ID_EVENTO = p_id_evento;
    IF NOT FOUND THEN RAISE EXCEPTION 'Evento não encontrado.'; END IF;
END;
$$;
