# db_project

Ambiente de desenvolvimento: WSL Ubuntu.

## Rotas e navegação

As páginas da aplicação foram organizadas em _blueprints_ modulares para facilitar manutenção e navegação:

- `admin`: painel administrativo e cadastros (`/admin/...`)
- `reports`: relatórios gerenciais (`/reports/...`)
- `staff`: fluxo operacional para funcionários (`/staff/...`)
- `internal`: portal de usuários internos USP (`/internal/...`)
- `external`: portal de convidados externos (`/external/...`)

Cada item do _sidebar_ utiliza o helper `build_url`, que tenta resolver o endpoint informado e registra um aviso no log da aplicação (`app.logger.warning`) se o endpoint não existir. Ao adicionar novas páginas, basta criar o endpoint no blueprint correspondente e referenciá-lo no template com `build_url('nome_do_endpoint')`.

## Como rodar

### 1. Instalar o Docker

Baixe e instale o Docker no seu sistema:

- [Docker Desktop para Windows/macOS](https://www.docker.com/products/docker-desktop)
- [Docker Engine para Linux](https://docs.docker.com/engine/install/)

Verifique a instalação:

```bash
docker --version
docker compose version
```

### 2. Baixar imagem do Postgres 17

```bash
docker pull postgres:17
```

### 3. Subir DB

Na pasta do repositório clonado

```bash
docker compose up -d
```

O serviço Flask ficará acessível em `http://127.0.0.1:5050/` (porta configurada no Docker).

### (Opcional) Acessar psql

```bash
docker exec -it postgres17 bash
su postgres
psql
```

### 4. Instalar dependências do Python

```
sudo apt install python3.12-venv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 5. Rodar testes

```
pytest -s
```

### 6. Executar o aplicativo Flask

Crie as variáveis de ambiente, se necessário, e execute:

```
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run --port 5050
```

O servidor local (fora dos contêineres) e o contêiner expõem a aplicação em `http://127.0.0.1:5050/`.

### 7. Popular o banco de dados com dados fictícios (carga completa)

1. **Gerar os arquivos SQL de carga**
   Acesse a pasta `dados_ficticios` e execute o script responsável por gerar os arquivos `.sql`:

   ```bash
   cd dados_ficticios
   python gerar_dados.py
   ```

   Esse script executa todos os geradores e move automaticamente os arquivos SQL criados para a pasta:

   ```
   sql/populate_mocked_full_db/
   ```

---

2. **Popular o banco de dados**
   Retorne à pasta principal do projeto e execute:

   ```bash
   python populate_db.py
   ```

   Esse comando aplicará as migrações de _schema_ e preencherá todas as tabelas do banco com os dados fictícios gerados.

---

3. **(Opcional) Reverter ou limpar o banco de dados**
   Caso queira desfazer a carga e remover os dados populados:

   ```bash
   python downgrade_db.py
   ```

   Isso executará os scripts de _downgrade_ na ordem inversa, limpando todas as tabelas e o schema.

---
