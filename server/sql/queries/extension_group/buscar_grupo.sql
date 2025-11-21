-- Query to select a extension group
-- Parameters:
--   %(nome_grupo)s - name of the extension group
-- Returns:
--   Queried extension group
SELECT * FROM grupo_extensao WHERE nome_grupo = %(nome_grupo)s;
