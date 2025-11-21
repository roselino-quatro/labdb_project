SELECT
    r.id_reserva,
    i.nome AS installation_name,
    r.data_reserva,
    r.horario_inicio,
    r.horario_fim,
    COALESCE(p.nome, 'Internal host not found') AS responsible_name
FROM reserva r
JOIN instalacao i ON i.id_instalacao = r.id_instalacao
LEFT JOIN pessoa p ON p.cpf = r.cpf_responsavel_interno
WHERE r.data_reserva >= CURRENT_DATE
ORDER BY r.data_reserva, r.horario_inicio
LIMIT 8;
