-- Query to check if a user exists by email or CPF
-- Parameters:
--   %(email_or_cpf)s - Email or CPF to check
-- Returns: User information if exists, NULL otherwise
SELECT
    cpf,
    nome,
    email,
    celular,
    data_nascimento
FROM pessoa
WHERE email = %(email_or_cpf)s OR cpf = %(email_or_cpf)s;
