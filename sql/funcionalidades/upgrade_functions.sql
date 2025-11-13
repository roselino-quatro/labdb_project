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

