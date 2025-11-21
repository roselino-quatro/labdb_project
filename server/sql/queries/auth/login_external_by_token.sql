-- Query to authenticate an external user by token
-- Parameters:
--   %(token)s - Token of the invite
SELECT authenticate_external_by_token(%(token)s) AS result;

