# Descrição dos Scripts e Fluxo de Geração de Dados

Este documento descreve a função de cada script Python, sua ordem de execução, principais entradas e saídas, além de observações práticas para rodar todo o processo.

---

## Como Rodar

### 1. Geração completa de dados
```bash
python gerar_dados.py
    - Roda todos os códigos python para gerar os arquivos
    - Preenche a pasta sql/populate_mocked_full_db com os arquivos sql para inserção de dados na base
    
    (opcional)
python	apagar_csvs_sqls.py
    - Apaga todos os arquivos csv e sql que estão dentro da pasta dados_ficticios
```
	

1. 01gerar_pessoas.py  
   - O que faz: gera um CSV com 10.000 pessoas fictícias.  
   - Saída principal: pessoas.csv (10.000 registros).

2. 02gerar_interno.py  
   - O que faz: recebe o CSV de pessoas e separa 90% para internos (interno_usp.csv) e 10% como pessoas_restantes.csv.  
   - Saídas: pessoas_internas.csv (90%), pessoas_restantes.csv (10%).

3. 03gerar_funcionario.py  
   - O que faz: lê pessoas_internas.csv, embaralha e seleciona 20% para gerar funcionários.  
   - Saídas: funcionarios.csv e upgrade_funcionario.sql (INSERTs em FUNCIONARIO).  
   - Observação: gera FORMACAO aleatória ao criar os INSERTs.

4. 04gerar_atribuicoes.py  
   - O que faz: para cada CPF em funcionarios.csv gera uma atribuição (FUNCIONARIO_ATRIBUICAO).  
   - Saídas: funcionario_atribuicao.csv e upgrade_funcionario_atribuicao.sql.

5. 05gerar_restricao.py  
   - O que faz: seleciona ~10% dos funcionários e atribui uma restrição física.  
   - Saídas: funcionario_restricao.csv e upgrade_funcionario_restricao.sql.

6. 06gerar_educador_fisico.py  
   - O que faz: seleciona ~10% dos funcionários para EDUCADOR_FISICO (gera número de conselho).  
   - Saídas: educador_fisico.csv e upgrade_educador_fisico.sql.

7. 07gerar_instalacao.py  
   - O que faz: gera uma lista de instalações (30 registros por combinação nome/tipo).  
   - Saídas: instalacoes.csv e upgrade_instalacao.sql.  
   - Observação: nomes/tipos são gerados de listas fixas; campos esperados no CSV: ID_INSTALACAO, NOME, TIPO, CAPACIDADE, EH_RESERVAVEL. Ver item "Melhorias" abaixo.

8. 08gerar_equipamento.py  
   - O que faz: gera equipamentos e registra em equipamentos.csv e SQL correspondente.  
   - Saídas: equipamentos.csv (usado por doações).

9. 09gerar_doacao_equipamento.py  
   - O que faz: usa pessoas_restantes.csv e equipamentos.csv para gerar doações (15% das pessoas_restantes, limitado por equipamentos disponíveis).  
   - Saídas: doacoes.csv e upgrade_doacao.sql.  
   - Observação: garante não duplicar equipamento em múltiplas doações.

10. 10gerar_reservas.py  
    - O que faz: usa pessoas_internas.csv e instalacoes.csv para gerar reservas (50% das pessoas_internas).  
    - Saídas: reservas.csv e upgrade_reserva.sql.  
    - Observação sobre cpf_responsavel_interno: o script escolhe responsáveis a partir de pessoas_internas.csv (qualquer interno), portanto não exige que o responsável seja funcionário. Se o banco exigir FK para FUNCIONARIO, o script precisa ser adaptado para escolher de funcionarios.csv (veja sugestão rápida abaixo).

11. 11gerar_atividade.py  
    - O que faz: gera atividades (por padrão 100) com ID_ATIVIDADE, NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO.  
    - Saídas: atividades.csv e upgrade_atividade.sql.

12. 12gerar_ocorrencia_semanal.py  
    - O que faz: para cada atividade gera 3 ocorrências semanais aleatórias (ID_INSTALACAO entre 1 e 30).  
    - Saídas: ocorrencias.csv e upgrade_ocorrencia_semanal.sql.

13. 13gerar_conduz_atividade.py  
    - O que faz: associa educadores físicos (educador_fisico.csv) a 1–5 atividades cada.  
    - Saídas: conduz_atividade.csv e upgrade_conduz_atividade.sql.

14. 14gerar_participacao_atividade.py  
    - O que faz: gera participações de pessoas_restantes.csv em atividades; 50% têm convidante interno (pessoas_internas.csv).  
    - Saídas: participacao_atividade.csv e upgrade_participacao_atividade.sql.  

15. 15gerar_evento.py  
    - O que faz: seleciona 50% das reservas para criar eventos com nome e descrição.  
    - Saídas: eventos.csv e upgrade_evento.sql.

16. 16gerar_supervisores_eventos.py  
    - O que faz: seleciona 80% dos eventos e atribui de 1 a 3 supervisores por evento (escolhidos em funcionarios.csv).  
    - Saídas: supervisao_evento.csv e upgrade_supervisao_evento.sql.

17. 17gerar_grupo_extensao.py  
    - O que faz: cria grupos de extensão com CPF_RESPONSAVEL_INTERNO vindo de pessoas_internas.csv.  
    - Saídas: grupos_extensao.csv e upgrade_grupo_extensao.sql.

18. 18gerar_atividade_grupo_extensao.py  
    - O que faz: associa cada grupo a 1–5 atividades aleatórias.  
    - Saídas: atividade_grupo_extensao.csv e upgrade_atividade_grupo_extensao.sql.

---

# Tabela de arquivos SQL gerados

1. upgrade_pessoa.sql  
2. upgrade_interno_usp.sql  
3. upgrade_funcionario.sql  
4. upgrade_funcionario_atribuicao.sql  
5. upgrade_funcionario_restricao.sql  
6. upgrade_educador_fisico.sql  
7. upgrade_instalacao.sql  
8. upgrade_equipamentos.sql (gerado pelo script 08)  
9. upgrade_doacao.sql  
10. upgrade_reserva.sql  
11. upgrade_atividade.sql  
12. upgrade_ocorrencia_semanal.sql  
13. upgrade_conduz_atividade.sql  
14. upgrade_participacao_atividade.sql  
15. upgrade_evento.sql  
16. upgrade_supervisao_evento.sql  
17. upgrade_grupo_extensao.sql  
18. upgrade_atividade_grupo_extensao.sql  

---

# Observações e Recomendações (pontos a ajustar)

- cpf_responsavel_interno (Tabela RESERVA):  
  - Implementação atual: o script 10 escolhe o responsável a partir de pessoas_internas.csv (qualquer pessoa interna).  
  - Recomendações: se o schema do banco exige que CPF_RESPONSAVEL_INTERNO seja um FUNCIONARIO, altere o script para escolher a partir de funcionarios.csv. Caso contrário, mantenha como pessoa interna.  

  Exemplo de mudança mínima (substituir leitura/seleção de responsáveis por leitura de funcionarios.csv):
  ```python
  # substituir leitura de 'pessoas_internas.csv' por:
  with open('funcionarios.csv', mode='r', encoding='utf-8') as f:
      next(csv.reader(f))  # pular cabeçalho
      funcionarios = [row[0] for row in csv.reader(f)]
  # e usar 'funcionarios' para escolher cpf_responsavel
  ```

- Geração de instalações (07gerar_instalacao.py):  
  - Atentar para a coerência entre NOME e TIPO (evitar combinações sem sentido se necessário).  

- Nomes e unicidade:  
  - Alguns scripts (15gerar_evento.py) adicionam sufixo para garantir unicidade; manter cuidado ao inserir no banco se houver restrição UNIQUE.

- Formatos de data/hora nos SQLs:  
  - Os scripts gravam datas/horários como strings no formato ISO (YYYY-MM-DD) e times via objeto time/string. Verificar compatibilidade com o SGBD alvo.

- Validações mínimas a agregar nos scripts (sugestões rápidas):  
  - Verificar existência dos arquivos de entrada e lançar erro amigável se ausentes.

---
