SELECT
    i.nome AS installation_name,
    COUNT(r.id_reserva) AS total_reservations,
    RANK() OVER (ORDER BY COUNT(r.id_reserva) DESC) AS ranking
FROM reserva r
JOIN instalacao i ON i.id_instalacao = r.id_instalacao
GROUP BY i.nome
ORDER BY ranking;
