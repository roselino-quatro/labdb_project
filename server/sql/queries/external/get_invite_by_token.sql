-- Query to get invite information by token
-- Parameters:
--   %(token)s - Token of the invite
SELECT
    ce.id_convite,
    ce.status,
    ce.nome_convidado,
    ce.documento_convidado,
    ce.email_convidado,
    ce.telefone_convidado,
    ce.id_atividade,
    ce.data_convite,
    ce.data_resposta,
    ce.observacoes,
    a.nome AS atividade_nome,
    a.data_inicio_periodo AS atividade_data_inicio,
    a.data_fim_periodo AS atividade_data_fim,
    a.vagas_limite AS atividade_vagas_limite
FROM convite_externo ce
LEFT JOIN atividade a ON a.id_atividade = ce.id_atividade
WHERE ce.token = %(token)s;
