-- Remover funções utilitárias
DROP FUNCTION IF EXISTS get_reservas_interno(VARCHAR);
DROP FUNCTION IF EXISTS get_instalacoes_disponiveis_horario(DATE, TIME, TIME);
DROP FUNCTION IF EXISTS get_atividades_educador(VARCHAR);
DROP FUNCTION IF EXISTS total_acessos_cefer(DATE, DATE);
DROP FUNCTION IF EXISTS listar_atividades(DATE, DIA_SEMANA, VARCHAR(100), VARCHAR(100));

-- Remover procedure
DROP PROCEDURE IF EXISTS cadastrar_evento(VARCHAR, TEXT, INT);
DROP PROCEDURE IF EXISTS inscrever_participante(VARCHAR(11), INT);