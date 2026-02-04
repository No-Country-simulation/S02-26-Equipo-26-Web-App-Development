CREATE OR REPLACE FUNCTION calcular_horas_guardia()
RETURNS TRIGGER AS $$
BEGIN
    NEW.horas_totales := EXTRACT(EPOCH FROM (NEW.hora_salida - NEW.hora_entrada)) / 3600;
    
    
    IF NEW.horas_totales < 0 THEN -- por si la guarida supera la media noche
        NEW.horas_totales := NEW.horas_totales + 24;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que activa la función automáticamente
CREATE TRIGGER tr_calcular_horas
BEFORE INSERT OR UPDATE ON guardias
FOR EACH ROW
EXECUTE FUNCTION calcular_horas_guardia();
