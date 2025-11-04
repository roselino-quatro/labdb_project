-- Remover funções utilitárias
DROP FUNCTION IF EXISTS verificar_capacidade_instalacao(INT) CASCADE;
DROP FUNCTION IF EXISTS get_reservas_interno(VARCHAR);
DROP FUNCTION IF EXISTS get_instalacoes_disponiveis_horario(DATE, TIME, TIME);
DROP FUNCTION IF EXISTS get_atividades_educador_fisico(VARCHAR);

-- Remover procedure
DROP PROCEDURE IF EXISTS cadastrar_evento(VARCHAR, TEXT, INT);