-- Query to authenticate a user and return their information and roles
-- Parameters:
--   %(email_or_cpf)s - Email or CPF of the user
--   %(password)s - Plain text password
--   %(ip_origin)s - IP address of the login attempt (optional)
SELECT authenticate_user(%(email_or_cpf)s, %(password)s, %(ip_origin)s) AS result;
