-- Query to create a registration request for an internal USP user
-- Parameters:
--   %(cpf_pessoa)s - CPF of the person
--   %(nusp)s - NUSP number
--   %(email)s - Email address
--   %(password)s - Plain text password
SELECT request_registration(%(cpf_pessoa)s, %(nusp)s, %(email)s, %(password)s) AS result;
