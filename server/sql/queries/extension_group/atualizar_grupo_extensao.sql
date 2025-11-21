-- Query to update a extension group
-- Parameters:
--   %(nome_grupo_antigo)s - old name of the extension group
--   %(nome_grupo_novo)s - new name of the extension group
--   %(descricao)s  -  new description of the group
--   %(cpf_responsavel)s  - cpf of the new responsible, must be a internal
CALL atualizar_grupo_extensao(%(nome_grupo_antigo)s, %(nome_grupo_novo)s,  %(descricao)s, %(cpf_responsavel)s);
