# db_project

Ambiente de desenvolvimento: WSL Ubuntu.

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

### 6. Popular o banco de dados com dados fictícios (carga completa)

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
