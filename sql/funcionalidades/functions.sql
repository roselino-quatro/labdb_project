-- FUNCTION para verificar a capacidade antes e criar reserva, retorna TRUE ou FALSE se é possível fazer reserva:
CREATE OR REPLACE FUNCTION verificar_capacidade_instalacao(p_id_instalacao INT)
RETURNS BOOLEAN AS $$
DECLARE
    capacidade INT;
    reservas INT;
BEGIN
    SELECT i.capacidade INTO capacidade
    FROM instalacao i WHERE i.id_instalacao = p_id_instalacao;

    SELECT COUNT(*) INTO reservas
    FROM reserva r WHERE r.id_instalacao = p_id_instalacao;

    RETURN reservas < capacidade;
END;
$$ LANGUAGE plpgsql;

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

-- SELECT * FROM get_instalacoes_disponiveis_horario('2025-11-10', '12:00', '14:00');

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


