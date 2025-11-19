-- Query to get user roles
-- Parameters:
--   %(cpf_pessoa)s - CPF of the user
-- Returns: JSON with roles array
SELECT get_user_roles(%(cpf_pessoa)s) AS result;
