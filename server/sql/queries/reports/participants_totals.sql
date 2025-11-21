SELECT
    a.nome AS activity_name,
    COUNT(pa.cpf_participante) AS total_participants
FROM participacao_atividade pa
JOIN atividade a ON a.id_atividade = pa.id_atividade
GROUP BY GROUPING SETS ((a.nome), ());
