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

-- PROCEDURES para criar atividades no sistema:
CREATE OR REPLACE PROCEDURE criar_atividade(
    p_nome VARCHAR,
    p_vagas INT,
    p_data_inicio DATE,
    p_data_fim DATE
) LANGUAGE plpgsql AS $$
BEGIN
    IF p_data_fim < p_data_inicio THEN
        RAISE EXCEPTION 'A data de término não pode ser anterior ao início.';
    END IF;

    INSERT INTO ATIVIDADE (NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO)
    VALUES (p_nome, p_vagas, p_data_inicio, p_data_fim);
END;
$$;

-- PROCEDURE para atualizar detalhes de uma atividade
CREATE OR REPLACE PROCEDURE atualizar_atividade(
    p_id_atividade INT,
    p_novo_nome VARCHAR,
    p_novas_vagas INT
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE ATIVIDADE
    SET NOME = p_novo_nome,
        VAGAS_LIMITE = p_novas_vagas
    WHERE ID_ATIVIDADE = p_id_atividade;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Atividade % não encontrada.', p_id_atividade;
    END IF;
END;
$$;

-- PROCEDURE para deletar uma atividade
CREATE OR REPLACE PROCEDURE deletar_atividade(p_id_atividade INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM ATIVIDADE WHERE ID_ATIVIDADE = p_id_atividade;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Atividade % não encontrada.', p_id_atividade;
    END IF;
END;
$$;

-- PROCEDURE para reservar uma instalação (Ex: Staff faz a reserva para um usuário)
CREATE OR REPLACE PROCEDURE reservar_instalacao(
    p_id_instalacao INT,
    p_cpf_responsavel VARCHAR,
    p_data DATE,
    p_hora_inicio TIME,
    p_hora_fim TIME
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO RESERVA (ID_INSTALACAO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM)
    VALUES (p_id_instalacao, p_cpf_responsavel, p_data, p_hora_inicio, p_hora_fim);
END;
$$;

-- PROCEDURE para cancelar uma reserva
CREATE OR REPLACE PROCEDURE cancelar_reserva_instalacao(p_id_reserva INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM RESERVA WHERE ID_RESERVA = p_id_reserva;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Reserva % não encontrada.', p_id_reserva;
    END IF;
END;
$$;

-- PROCEDURE para reservar equipamento
CREATE OR REPLACE PROCEDURE reservar_equipamento(
    p_id_equipamento VARCHAR,
    p_cpf_responsavel VARCHAR,
    p_data DATE,
    p_hora_inicio TIME,
    p_hora_fim TIME
) LANGUAGE plpgsql AS $$
BEGIN
    -- Verifica se o equipamento é reservável (Regra de Negócio)
    PERFORM 1 FROM EQUIPAMENTO 
    WHERE ID_PATRIMONIO = p_id_equipamento AND EH_RESERVAVEL = 'N';
    
    IF FOUND THEN
        RAISE EXCEPTION 'O equipamento % não é reservável (uso livre ou interno).', p_id_equipamento;
    END IF;

    INSERT INTO RESERVA_EQUIPAMENTO (ID_EQUIPAMENTO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM)
    VALUES (p_id_equipamento, p_cpf_responsavel, p_data, p_hora_inicio, p_hora_fim);
END;
$$;

-- PROCEDURE para cancelar reserva de equipamento
CREATE OR REPLACE PROCEDURE cancelar_reserva_equipamento(p_id_reserva_equip INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM RESERVA_EQUIPAMENTO WHERE ID_RESERVA_EQUIP = p_id_reserva_equip;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Reserva de equipamento % não encontrada.', p_id_reserva_equip;
    END IF;
END;
$$;

-- PROCEDURE para inscrever participante em atividade com verificação de vagas:
CREATE OR REPLACE PROCEDURE inscrever_participante_atividade(
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

-- PROCEDURE para remover um participante de uma atividade
CREATE OR REPLACE PROCEDURE remover_participante_atividade(
    p_cpf_participante VARCHAR,
    p_id_atividade INT
) LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM PARTICIPACAO_ATIVIDADE
    WHERE CPF_PARTICIPANTE = p_cpf_participante
      AND ID_ATIVIDADE = p_id_atividade;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Participante % não encontrado na atividade %.', p_cpf_participante, p_id_atividade;
    END IF;
END;
$$;