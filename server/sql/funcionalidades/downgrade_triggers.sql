-- Remover triggers
DROP TRIGGER IF EXISTS trg_validar_horario_reserva ON reserva;
DROP TRIGGER IF EXISTS trg_checar_formacao_educador ON conduz_atividade;

-- Remover funções associadas aos triggers
DROP FUNCTION IF EXISTS validar_horario_reserva() CASCADE;
DROP FUNCTION IF EXISTS checar_formacao_educador() CASCADE;