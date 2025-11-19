-- Query to reject a registration request
-- Parameters:
--   %(id_solicitacao)s - ID of the registration request
--   %(cpf_admin)s - CPF of the admin rejecting the request
--   %(observacoes)s - Optional rejection reason
SELECT reject_registration(%(id_solicitacao)s, %(cpf_admin)s, %(observacoes)s) AS result;
