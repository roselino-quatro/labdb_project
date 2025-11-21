-- Query to create new extension group
-- Parameters:
--   %(nome_grupo)s - name of the extension group
--   %(descricao)s  - description of the group
--   %(cpf_responsavel)s  - cpf of the responsible, must be a internal
CALL criar_grupo_extensao(%(nome_grupo)s, %(descricao)s, %(cpf_responsavel)s);
