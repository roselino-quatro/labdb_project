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
BEGIN
    UPDATE GRUPO_EXTENSAO
    SET NOME_GRUPO = p_nome_novo,
        DESCRICAO = p_descricao_nova,
        CPF_RESPONSAVEL_INTERNO = p_cpf_responsavel_novo 
    WHERE NOME_GRUPO = p_nome_antigo;
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
    p_nome VARCHAR,
    p_id_instalacao INT,
    p_eh_reservavel CHAR
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE EQUIPAMENTO
    SET NOME = p_nome,
        ID_INSTALACAO_LOCAL = p_id_instalacao,
        EH_RESERVAVEL = p_eh_reservavel
    WHERE ID_PATRIMONIO = p_id_patrimonio;
    
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
    p_nome VARCHAR,
    p_capacidade INT,
    p_eh_reservavel CHAR
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE INSTALACAO
    SET NOME = p_nome, CAPACIDADE = p_capacidade, EH_RESERVAVEL = p_eh_reservavel
    WHERE ID_INSTALACAO = p_id;
    
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
BEGIN
    UPDATE EVENTO
    SET NOME = p_nome_novo,
        DESCRICAO = p_descricao_nova
    WHERE ID_EVENTO = p_id_evento;

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