#!/bin/bash
# Script para fazer downgrade do banco de dados (remover dados e schema)
# Executa o script Python data_generators/downgrade.py
# Deve ser executado a partir da raiz do projeto ou via scripts/downgrade_db.sh

# Obter o diretório onde o script está localizado
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Mudar para a raiz do projeto para garantir que os imports do Python funcionem
cd "$PROJECT_ROOT"

echo "=== Executando Script de Downgrade de Banco de Dados ==="
echo "Diretório de execução: $(pwd)"

# Configurar PYTHONPATH para incluir a raiz do projeto
export PYTHONPATH="${PYTHONPATH}:${PROJECT_ROOT}"

# Executar o script Python
python data_generators/downgrade.py
