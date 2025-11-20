#!/bin/bash
# Script para popular o banco de dados
# Executa o script Python data_generators/populate.py
# Deve ser executado a partir da raiz do projeto ou via scripts/populate_db.sh

# Obter o diretório onde o script está localizado
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Mudar para a raiz do projeto para garantir que os imports do Python funcionem
cd "$PROJECT_ROOT"

echo "=== Executando Script de População de Banco de Dados ==="
echo "Diretório de execução: $(pwd)"

# Configurar PYTHONPATH para incluir a raiz do projeto
export PYTHONPATH="${PYTHONPATH}:${PROJECT_ROOT}"

# Executar o script Python
python data_generators/populate.py
