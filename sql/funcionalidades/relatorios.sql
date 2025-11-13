-- ROLL UP para contar reservas por instalação, mês e total geral:
SELECT 
    i.nome AS nome_instalacao,
    EXTRACT(MONTH FROM r.data_reserva) AS mes,
    COUNT(*) AS total_reservas
FROM reserva r
JOIN instalacao i ON i.id_instalacao = r.id_instalacao
GROUP BY ROLLUP (i.nome, EXTRACT(MONTH FROM r.data_reserva))
ORDER BY i.nome, mes;

-- CUBE para mostrar total de atividades conduzidas por educador e categoria:
SELECT 
    e.numero_conselho,
    iu.categoria,
    COUNT(a.id_atividade) AS total_atividades
FROM conduz_atividade ca
JOIN educador_fisico e ON ca.cpf_educador_fisico = e.cpf_funcionario
JOIN funcionario f ON f.cpf_interno = e.cpf_funcionario
JOIN interno_usp iu ON iu.cpf_pessoa = f.cpf_interno
JOIN atividade a ON a.id_atividade = ca.id_atividade
GROUP BY CUBE (e.numero_conselho, iu.categoria)
ORDER BY e.numero_conselho, iu.categoria;

-- GROUPING SETS para total de participantes por atividade e total geral:
SELECT 
    a.nome AS atividade,
    COUNT(pa.cpf_participante) AS total_participantes
FROM participacao_atividade pa
JOIN atividade a ON a.id_atividade = pa.id_atividade
GROUP BY GROUPING SETS ((a.nome), ());

-- WINDOW FUNCTION para ranking de instalações mais reservadas:
SELECT 
    i.nome,
    COUNT(r.id_reserva) AS total_reservas,
    RANK() OVER (ORDER BY COUNT(r.id_reserva) DESC) AS posicao
FROM reserva r
JOIN instalacao i ON i.id_instalacao = r.id_instalacao
GROUP BY i.nome;

-- Total de reservas e duração total por instalação
SELECT 
    i.NOME AS NOME_INSTALACAO,
    COUNT(r.ID_RESERVA) AS NUM_RESERVAS,
    SUM(EXTRACT(EPOCH FROM (r.HORARIO_FIM - r.HORARIO_INICIO)) / 3600) AS DURACAO_TOTAL_HORAS
FROM 
    RESERVA r
JOIN 
    INSTALACAO i ON r.ID_INSTALACAO = i.ID_INSTALACAO
GROUP BY 
    i.NOME
ORDER BY 
    NUM_RESERVAS DESC, DURACAO_TOTAL_HORAS DESC;
