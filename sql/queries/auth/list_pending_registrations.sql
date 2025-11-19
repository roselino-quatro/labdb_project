-- Query to list all pending registration requests
-- Returns: List of pending registration requests with user information
SELECT
    sc.id_solicitacao,
    sc.cpf_pessoa,
    p.nome,
    p.email,
    sc.nusp,
    sc.data_solicitacao,
    sc.observacoes
FROM solicitacao_cadastro sc
JOIN pessoa p ON sc.cpf_pessoa = p.cpf
WHERE sc.status = 'PENDENTE'
ORDER BY sc.data_solicitacao ASC;
