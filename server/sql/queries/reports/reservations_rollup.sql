SELECT
    i.nome AS installation_name,
    EXTRACT(MONTH FROM r.data_reserva) AS month_number,
    COUNT(*) AS total_reservations
FROM reserva r
JOIN instalacao i ON i.id_instalacao = r.id_instalacao
GROUP BY ROLLUP (i.nome, EXTRACT(MONTH FROM r.data_reserva))
ORDER BY i.nome, month_number;
