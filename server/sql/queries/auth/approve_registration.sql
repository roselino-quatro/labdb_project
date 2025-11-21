-- Query to approve a registration request and create user account
-- Parameters:
--   %(id_solicitacao)s - ID of the registration request
--   %(cpf_admin)s - CPF of the admin approving the request
SELECT approve_registration(%(id_solicitacao)s, %(cpf_admin)s) AS result;
