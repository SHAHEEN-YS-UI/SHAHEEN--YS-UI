# SHAHEEN-YS-UI

A professionally branded derivative of Open WebUI — a modern self-hosted AI workspace supporting multiple AI providers, AI agents, MCP servers, tools, workflows, RAG, and enterprise deployment.

## Stack

- **Frontend**: SvelteKit + Tailwind CSS (built to `build/` directory)
- **Backend**: Python / FastAPI + SQLAlchemy (in `backend/open_webui/`)
- **Database**: SQLite (dev) or PostgreSQL via `DATABASE_URL` (Railway/prod)
- **Package manager**: npm (frontend), pip/uv (backend)

## Running locally

The app is a unified Python server that serves the pre-built SvelteKit frontend.

```bash
# Install backend deps
cd backend && pip install -e ".[all]"

# Build frontend
npm install && npm run build

# Start server
bash backend/start.sh
```

Or with Docker:
```bash
docker compose up -d
```

## Key environment variables

| Variable | Purpose |
|---|---|
| `WEBUI_NAME` | Display name (default: `SHAHEEN-YS-UI`) |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI key |
| `ANTHROPIC_API_KEY` | Anthropic Claude key |
| `GEMINI_API_KEY` | Google Gemini key |
| `GROQ_API_KEY` | Groq key |
| `MISTRAL_API_KEY` | Mistral key |
| `OPENROUTER_API_KEY` | OpenRouter key |
| `XAI_API_KEY` | xAI / Grok key |
| `DEEPSEEK_API_KEY` | DeepSeek key |
| `ENABLE_AIDER` | Set `true` to enable Aider coding assistant |
| `PORT` | Server port (default: 8080) |

See `.env.example` for the full list.

## Railway deployment

Pre-configured via `railway.toml`. Push to GitHub and connect to Railway — it will build via Dockerfile and deploy automatically. Set all environment variables in the Railway dashboard.

## Project structure

```
backend/open_webui/   FastAPI application
  main.py             App entrypoint + lifespan
  env.py              All environment variable declarations
  config.py           Runtime config management
  routers/            API route handlers
  models/             SQLAlchemy models
  aider_integration.py  Aider coding assistant integration

src/                  SvelteKit frontend
  lib/constants.ts    APP_NAME and base URLs
  lib/components/     UI components
  routes/             SvelteKit pages

static/static/        Static assets (icons, manifest, etc.)
railway.toml          Railway deployment config
```

## User Preferences

- Keep all branding as SHAHEEN-YS-UI (not Open WebUI)
- Load all secrets from environment variables only — never hardcode
- Preserve existing architecture and APIs
- Railway + Docker deployment must remain functional
