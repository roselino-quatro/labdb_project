#!/bin/bash

# Script para rodar Flask e Next.js em modo desenvolvimento usando tmux

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

# Verificar se tmux está instalado
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Erro: tmux não está instalado${NC}"
    echo -e "${YELLOW}Instale com: brew install tmux (macOS) ou sudo apt install tmux (Linux)${NC}"
    exit 1
fi

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

# Matar sessão tmux existente se houver
tmux kill-session -t cefer-dev 2>/dev/null || true

# Criar nova sessão tmux
echo -e "${GREEN}Criando sessão tmux 'cefer-dev'...${NC}"
tmux new-session -d -s cefer-dev

# Configurar variáveis de ambiente para Flask
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5050
export FLASK_DEBUG=1
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=public
export DB_USER=postgres
export DB_PASSWORD=password

# Painel 0: Flask
tmux rename-window -t cefer-dev:0 'Flask'
tmux send-keys -t cefer-dev:0 "cd $SERVER_DIR" C-m

# Ativar ambiente virtual
if [ -d "$SERVER_DIR/venv" ]; then
    tmux send-keys -t cefer-dev:0 "source venv/bin/activate" C-m
elif [ -d "$SERVER_DIR/env" ]; then
    tmux send-keys -t cefer-dev:0 "source env/bin/activate" C-m
fi

tmux send-keys -t cefer-dev:0 "export FLASK_APP=wsgi.py FLASK_ENV=development FLASK_RUN_PORT=5050 FLASK_DEBUG=1" C-m
tmux send-keys -t cefer-dev:0 "export DB_HOST=localhost DB_PORT=5432 DB_NAME=public DB_USER=postgres DB_PASSWORD=password" C-m
tmux send-keys -t cefer-dev:0 "flask run --host=0.0.0.0 --port=5050 --reload" C-m

# Painel 1: Next.js
tmux new-window -t cefer-dev:1 -n 'Next.js'
tmux send-keys -t cefer-dev:1 "cd $INTERFACE_DIR" C-m
tmux send-keys -t cefer-dev:1 "export NEXT_PUBLIC_API_URL=http://localhost:5050" C-m

if command -v pnpm &> /dev/null; then
    tmux send-keys -t cefer-dev:1 "pnpm dev" C-m
elif command -v npm &> /dev/null; then
    tmux send-keys -t cefer-dev:1 "npm run dev" C-m
fi

# Voltar para o primeiro painel
tmux select-window -t cefer-dev:0

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Servidores iniciados no tmux!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${BLUE}Flask:${NC} http://localhost:5050"
echo -e "${BLUE}Next.js:${NC} http://localhost:3000"
echo -e "\n${YELLOW}Comandos úteis:${NC}"
echo -e "  ${BLUE}tmux attach -t cefer-dev${NC}  - Anexar à sessão"
echo -e "  ${BLUE}tmux kill-session -t cefer-dev${NC}  - Encerrar sessão"
echo -e "  ${BLUE}Ctrl+B, depois número${NC}  - Alternar entre painéis"
echo -e "  ${BLUE}Ctrl+B, depois D${NC}  - Desanexar da sessão"
echo -e "\n${GREEN}Anexando à sessão tmux...${NC}\n"

# Anexar à sessão
tmux attach -t cefer-dev
