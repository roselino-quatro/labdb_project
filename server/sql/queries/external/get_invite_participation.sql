-- Query to get participation information for an external invite
-- Parameters:
--   %(invite_id)s - ID of the invite
-- Note: This query checks if there's a participation where:
--   1. The activity matches the invite's activity
--   2. The participant CPF matches the invite's document (DOCUMENTO_CONVIDADO)
SELECT
    pa.cpf_participante,
    pa.id_atividade,
    pa.data_inscricao,
    a.nome AS atividade_nome,
    a.data_inicio_periodo AS atividade_data_inicio,
    a.data_fim_periodo AS atividade_data_fim,
    a.vagas_limite AS atividade_vagas_limite
FROM participacao_atividade pa
JOIN atividade a ON a.id_atividade = pa.id_atividade
JOIN convite_externo ce ON ce.id_atividade = pa.id_atividade
WHERE ce.id_convite = %(invite_id)s
AND ce.documento_convidado = pa.cpf_participante;
