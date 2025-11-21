SELECT
    participant.nome AS participant_name,
    participant.email AS participant_email,
    atividade.nome AS activity_name,
    host.nome AS host_name,
    iu_host.nusp AS host_nusp
FROM participacao_atividade pa
JOIN pessoa participant ON participant.cpf = pa.cpf_participante
JOIN atividade ON atividade.id_atividade = pa.id_atividade
JOIN interno_usp iu_host ON iu_host.cpf_pessoa = pa.cpf_convidante_interno
JOIN pessoa host ON host.cpf = iu_host.cpf_pessoa
LEFT JOIN interno_usp iu_participant ON iu_participant.cpf_pessoa = pa.cpf_participante
WHERE iu_participant.cpf_pessoa IS NULL
ORDER BY atividade.nome, participant.nome;
