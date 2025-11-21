#!/bin/bash

# Script para rodar Flask e Next.js em modo desenvolvimento

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretórios
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVER_DIR="$PROJECT_ROOT/server"
INTERFACE_DIR="$PROJECT_ROOT/interface"

# Função para limpar processos ao sair
cleanup() {
    echo -e "\n${YELLOW}Encerrando processos...${NC}"
    if [ ! -z "$FLASK_PID" ]; then
        kill $FLASK_PID 2>/dev/null || true
    fi
    if [ ! -z "$NEXTJS_PID" ]; then
        kill $NEXTJS_PID 2>/dev/null || true
    fi
    exit 0
}

# Trap para limpar ao receber SIGINT ou SIGTERM
trap cleanup SIGINT SIGTERM

# Verificar se o PostgreSQL está rodando
echo -e "${BLUE}Verificando PostgreSQL...${NC}"
if ! pg_isready -h localhost -p 5432 -U postgres > /dev/null 2>&1; then
    echo -e "${YELLOW}PostgreSQL não está rodando. Iniciando com Docker...${NC}"
    cd "$PROJECT_ROOT"
    docker compose up -d postgres
    echo -e "${BLUE}Aguardando PostgreSQL estar pronto...${NC}"
    sleep 5
fi

# Verificar se as dependências Python estão instaladas
if [ ! -d "$SERVER_DIR/venv" ] && [ ! -d "$SERVER_DIR/env" ]; then
    echo -e "${YELLOW}Ambiente virtual Python não encontrado. Criando...${NC}"
    cd "$SERVER_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Ativar ambiente virtual Python
if [ -d "$SERVER_DIR/venv" ]; then
    source "$SERVER_DIR/venv/bin/activate"
elif [ -d "$SERVER_DIR/env" ]; then
    source "$SERVER_DIR/env/bin/activate"
fi

# Verificar se as dependências Node.js estão instaladas
if [ ! -d "$INTERFACE_DIR/node_modules" ]; then
    echo -e "${YELLOW}Dependências Node.js não encontradas. Instalando...${NC}"
    cd "$INTERFACE_DIR"
    if command -v pnpm &> /dev/null; then
        pnpm install
    elif command -v npm &> /dev/null; then
        npm install
    else
        echo -e "${RED}Erro: pnpm ou npm não encontrado${NC}"
        exit 1
    fi
fi

# Configurar variáveis de ambiente
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5050
export FLASK_DEBUG=1
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=public
export DB_USER=postgres
export DB_PASSWORD=password

# Iniciar Flask
echo -e "${GREEN}Iniciando Flask na porta 5050...${NC}"
cd "$SERVER_DIR"
flask run --host=0.0.0.0 --port=5050 --reload &
FLASK_PID=$!

# Aguardar Flask iniciar
sleep 3

# Iniciar Next.js
echo -e "${GREEN}Iniciando Next.js na porta 3000...${NC}"
cd "$INTERFACE_DIR"
export NEXT_PUBLIC_API_URL=http://localhost:5050
if command -v pnpm &> /dev/null; then
    pnpm dev &
elif command -v npm &> /dev/null; then
    npm run dev &
else
    echo -e "${RED}Erro: pnpm ou npm não encontrado${NC}"
    kill $FLASK_PID 2>/dev/null || true
    exit 1
fi
NEXTJS_PID=$!

# Aguardar Next.js iniciar
sleep 3

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Servidores iniciados com sucesso!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${BLUE}Flask:${NC} http://localhost:5050"
echo -e "${BLUE}Next.js:${NC} http://localhost:3000"
echo -e "\n${YELLOW}Pressione Ctrl+C para encerrar${NC}\n"

# Aguardar processos
wait
