-- Query to check if a registration request already exists for a CPF/NUSP
-- Parameters:
--   %(cpf_pessoa)s - CPF to check
--   %(nusp)s - NUSP to check
-- Returns: Request information if exists, NULL otherwise
SELECT
    id_solicitacao,
    cpf_pessoa,
    nusp,
    status,
    data_solicitacao
FROM solicitacao_cadastro
WHERE cpf_pessoa = %(cpf_pessoa)s
AND nusp = %(nusp)s
AND status = 'PENDENTE';
