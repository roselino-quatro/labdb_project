# Programas de Interação com o Banco de Dados

## Programa `tela_relatorios.py`

Este programa retorna alguns dados referentes a consultas específicas no banco de dados.  

---

## Programa `tela_funcoes.py`

Este programa permite interagir com o banco de dados PostgreSQL para consultar informações sobre instalações, reservas, eventos e atividades de educadores físicos.

> **Observação:** Todas as funções e procedures usadas pelo programa devem estar previamente implementadas no banco de dados.

## Requisitos

- Bibliotecas:
  - `psycopg2`
  - `tabulate`

Instalação das bibliotecas:

```bash
pip install psycopg2 tabulate
```

## 1 - Verificar capacidade de instalação
- ID da instalação: 5 → resposta: TRUE  
- ID da instalação: 1 → resposta: FALSE  

---

## 2 - Cadastrar evento
- Nome do evento: DANÇA TESTE 123  
- Descrição: testando  
- ID da reserva: 2755  

---

## 3 - Ver reservas de um interno USP
- CPF do interno: 69355642988  

---

## 4 - Listar instalações disponíveis em determinado dia e horário
- Data (YYYY-MM-DD): 2023-05-12  
- Hora início (HH:MM): 12:00  
- Hora fim (HH:MM): 14:00  

---

## 5 - Listar atividades de um educador físico
- CPF do educador físico: 40505965399  


