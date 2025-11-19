-- TRIGGER para impedir reserva fora do horário permitido:
CREATE OR REPLACE FUNCTION validar_horario_reserva()
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.horario_inicio < '06:00' OR NEW.horario_fim > '22:00') THEN
        RAISE EXCEPTION 'Horário de reserva inválido (permitido: 06h–22h)';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_horario_reserva
BEFORE INSERT OR UPDATE ON reserva
FOR EACH ROW EXECUTE FUNCTION validar_horario_reserva();

-- TRIGGER para impedir que educador conduza atividade sem formação:
CREATE OR REPLACE FUNCTION checar_formacao_educador()
RETURNS TRIGGER AS $$
DECLARE
    formacao TEXT;
BEGIN
    SELECT f.formacao INTO formacao
    FROM funcionario f
    WHERE f.cpf_interno = NEW.cpf_educador_fisico;

    IF formacao IS NULL THEN
        RAISE EXCEPTION 'O educador físico precisa ter uma formação cadastrada';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_checar_formacao_educador
BEFORE INSERT ON conduz_atividade
FOR EACH ROW EXECUTE FUNCTION checar_formacao_educador();
