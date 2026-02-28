# Mari-Olivier (Flask + Railway)

Plataforma de vídeos com login + painel admin para cadastrar Temporadas e Episódios (links do YouTube).

## Rodar local
```bash
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask --app app run --debug
```

Acesse:
- `http://127.0.0.1:5000/auth/login`
- Admin é criado automaticamente usando `ADMIN_EMAIL`/`ADMIN_PASSWORD` do `.env`.

## Deploy no Railway (via GitHub)
1. Suba este repositório no GitHub
2. No Railway: New Project → Deploy from GitHub
3. Configure variáveis:
   - `SECRET_KEY`
   - `DATABASE_URL` (Railway Postgres)
   - `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_NAME`
4. Railway detecta `Procfile` e sobe com `gunicorn`.

## Observações sobre YouTube "privado"
YouTube *privado* (não listado como "unlisted") normalmente não toca em embed sem login do Google.
Este projeto suporta links **não listados** (unlisted) ou links públicos.
