SELECT
    id_atividade,
    nome_atividade,
    grupo_extensao,
    dia_semana::text AS weekday,
    horario_inicio,
    horario_fim,
    vagas_ocupadas,
    vagas_limite,
    CASE
        WHEN vagas_limite IS NULL OR vagas_limite = 0 THEN 0
        ELSE ROUND((vagas_ocupadas::numeric / vagas_limite) * 100, 1)
    END AS occupancy_rate
FROM listar_atividades(NULL, NULL, NULL)
ORDER BY vagas_ocupadas DESC NULLS LAST
LIMIT 8;
