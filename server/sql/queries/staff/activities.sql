SELECT
    id_atividade,
    nome_atividade,
    grupo_extensao,
    dia_semana::text AS weekday,
    horario_inicio,
    horario_fim,
    vagas_ocupadas,
    vagas_limite
FROM listar_atividades(%(weekday)s, %(group_name)s, %(modality)s)
ORDER BY dia_semana, horario_inicio;
