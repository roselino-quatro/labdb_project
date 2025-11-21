# Descrição dos Scripts e Fluxo de Geração de Dados

Este documento descreve a função de cada script Python, sua ordem de execução, principais entradas e saídas, além de observações práticas para rodar todo o processo.

## Estrutura Organizada por Domínios

Os scripts estão organizados em pastas por domínio de negócio:

- **pessoas/**: Scripts relacionados a pessoas, internos, funcionários e suas características
- **infraestrutura/**: Scripts relacionados a instalações, equipamentos e doações
- **reservas/**: Scripts relacionados a reservas de instalações e equipamentos
- **atividades/**: Scripts relacionados a atividades, ocorrências e participações
- **eventos/**: Scripts relacionados a eventos e supervisão
- **grupos/**: Scripts relacionados a grupos de extensão

---

## Como Rodar

### Geração completa de dados
```bash
python populate_db.py
```

Este comando cria o schema e executa todos os geradores na ordem correta de dependência, inserindo os dados diretamente no banco de dados.

---

## Scripts por Domínio

### Domínio: Pessoas

1. **01gerar_pessoas.py**
   - O que faz: gera 10.000 pessoas fictícias e insere diretamente no banco.
   - Tabela: PESSOA

2. **02gerar_interno_usp.py**
   - O que faz: seleciona 90% das pessoas para criar internos USP.
   - Tabela: INTERNO_USP

3. **03gerar_funcionario.py**
   - O que faz: seleciona 20% dos internos para criar funcionários.
   - Tabela: FUNCIONARIO

4. **04gerar_atribuicoes.py**
   - O que faz: gera uma atribuição para cada funcionário.
   - Tabela: FUNCIONARIO_ATRIBUICAO

5. **05gerar_restricao.py**
   - O que faz: seleciona ~10% dos funcionários e atribui uma restrição física.
   - Tabela: FUNCIONARIO_RESTRICAO

6. **06gerar_educador_fisico.py**
   - O que faz: seleciona ~10% dos funcionários para criar educadores físicos.
   - Tabela: EDUCADOR_FISICO

### Domínio: Infraestrutura

7. **07gerar_instalacao.py**
   - O que faz: gera instalações únicas e coerentes (quadras, piscinas, academias, etc.).
   - Tabela: INSTALACAO

8. **08gerar_equipamento.py**
   - O que faz: gera equipamentos e os associa a instalações.
   - Tabela: EQUIPAMENTO

9. **09gerar_doacao_equipamento.py**
   - O que faz: gera doações de equipamentos por pessoas não-internas.
   - Tabela: DOACAO

### Domínio: Reservas

10. **10gerar_reservas.py**
    - O que faz: gera reservas de instalações por 50% dos internos.
    - Tabela: RESERVA

19. **19gerar_reserva_equipamento.py**
    - O que faz: gera reservas de equipamentos reserváveis.
    - Tabela: RESERVA_EQUIPAMENTO

### Domínio: Atividades

11. **11gerar_atividade.py**
    - O que faz: gera atividades com períodos e vagas.
    - Tabela: ATIVIDADE

12. **12gerar_ocorrencia_semanal.py**
    - O que faz: gera 3 ocorrências semanais para cada atividade.
    - Tabela: OCORRENCIA_SEMANAL

13. **13gerar_conduz_atividade.py**
    - O que faz: associa educadores físicos a 1–5 atividades cada.
    - Tabela: CONDUZ_ATIVIDADE

14. **14gerar_participacao_atividade.py**
    - O que faz: gera participações de pessoas não-internas em atividades.
    - Tabela: PARTICIPACAO_ATIVIDADE

### Domínio: Eventos

15. **15gerar_evento.py**
    - O que faz: seleciona 50% das reservas para criar eventos.
    - Tabela: EVENTO

16. **16gerar_supervisores_eventos.py**
    - O que faz: seleciona 80% dos eventos e atribui 1–3 supervisores por evento.
    - Tabela: SUPERVISAO_EVENTO

### Domínio: Grupos

17. **17gerar_grupo_extensao.py**
    - O que faz: cria grupos de extensão com responsáveis internos.
    - Tabela: GRUPO_EXTENSAO

18. **18gerar_atividade_grupo_extensao.py**
    - O que faz: associa grupos a atividades de forma semântica.
    - Tabela: ATIVIDADE_GRUPO_EXTENSAO

---

## Observações Importantes

- Todos os scripts inserem dados **diretamente no banco de dados**, não geram mais arquivos CSV ou SQL intermediários.
- A ordem de execução é crítica devido às dependências entre as tabelas.
- Os scripts são executados automaticamente pelo `populate_db.py` na ordem correta.
- Cada domínio está isolado em sua própria pasta para facilitar manutenção e compreensão.

---

## Dependências entre Domínios

1. **Pessoas** → Base para todos os outros domínios
2. **Infraestrutura** → Necessário para reservas e atividades
3. **Reservas** → Depende de Pessoas e Infraestrutura
4. **Atividades** → Depende de Pessoas e Infraestrutura
5. **Eventos** → Depende de Reservas
6. **Grupos** → Depende de Pessoas e Atividades
