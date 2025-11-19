WITH stats AS (
    SELECT
        'Pessoas'::text AS label,
        COUNT(*)::int AS value,
        'Pessoas registradas'::text AS description
    FROM pessoa
    UNION ALL
    SELECT
        'Membros internos'::text,
        COUNT(*)::int,
        'Comunidade interna USP'::text
    FROM interno_usp
    UNION ALL
    SELECT
        'Reservas'::text,
        COUNT(*)::int,
        'Reservas agendadas'::text
    FROM reserva
    UNION ALL
    SELECT
        'Atividades'::text,
        COUNT(*)::int,
        'Atividades registradas'::text
    FROM atividade
)
SELECT label, value, description
FROM stats;
