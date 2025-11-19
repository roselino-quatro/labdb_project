-- Remover funções utilitárias
DROP FUNCTION IF EXISTS get_reservas_interno(VARCHAR);
DROP FUNCTION IF EXISTS get_instalacoes_disponiveis_horario(DATE, TIME, TIME);
DROP FUNCTION IF EXISTS get_atividades_educador(VARCHAR);
DROP FUNCTION IF EXISTS total_acessos_cefer(DATE, DATE);
DROP FUNCTION IF EXISTS listar_atividades(DATE, DIA_SEMANA, VARCHAR(100), VARCHAR(100));

-- Remover procedure
DROP PROCEDURE IF EXISTS cadastrar_evento(VARCHAR, TEXT, INT);
DROP PROCEDURE IF EXISTS inscrever_participante(VARCHAR(11), INT);

-- Remover funções de autenticação
DROP FUNCTION IF EXISTS authenticate_user(VARCHAR, TEXT, VARCHAR);
DROP FUNCTION IF EXISTS reject_registration(INT, VARCHAR, TEXT);
DROP FUNCTION IF EXISTS approve_registration(INT, VARCHAR);
DROP FUNCTION IF EXISTS request_registration(VARCHAR, VARCHAR, VARCHAR, TEXT);
DROP FUNCTION IF EXISTS get_user_roles(VARCHAR);
DROP FUNCTION IF EXISTS verify_password(TEXT, TEXT);
DROP FUNCTION IF EXISTS hash_password(TEXT);
