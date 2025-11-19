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

