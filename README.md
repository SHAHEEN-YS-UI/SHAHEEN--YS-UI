<div align="center">

<img src="https://i.postimg.cc/jSgqxtPt/Picsart-26-07-19-04-27-01-342.png" width="600" alt="SHAHEEN-YS-UI Banner" />

# SHAHEEN-YS-UI

**Enterprise AI Workspace — Unified Intelligence Platform**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-5-FF3E00.svg)](https://kit.svelte.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://docker.com)
[![Railway](https://img.shields.io/badge/Railway-deployed-0B0D0E.svg)](https://railway.app)
[![OpenAI](https://img.shields.io/badge/OpenAI-compatible-412991.svg)](https://openai.com)
[![Anthropic](https://img.shields.io/badge/Anthropic-Claude-CC785C.svg)](https://anthropic.com)
[![Production Ready](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

</div>

---

## 🚀 SHAHEEN-YS-UI

A professionally branded, enterprise-grade AI workspace built on the Open WebUI platform. SHAHEEN-YS-UI brings every major AI provider under one roof — locally or in the cloud — with automatic provider discovery, multi-key load balancing, and a world-class admin experience.

---

## 🌌 About

SHAHEEN-YS-UI is a self-hosted AI hub supporting simultaneous connections to OpenAI, Anthropic Claude, Google Gemini, Groq, Mistral, xAI Grok, DeepSeek, OpenRouter, Ollama, and any OpenAI-compatible endpoint. No vendor lock-in. No manual configuration required after deployment — just set your API keys and every available provider auto-registers.

---

## ✨ Overview

| Capability | Details |
|---|---|
| **AI Providers** | OpenAI, Anthropic, Gemini, Groq, Mistral, xAI, DeepSeek, OpenRouter, Ollama, Azure OpenAI, LM Studio + any OpenAI-compatible API |
| **Model Types** | LLM Chat, Image Generation, Text-to-Speech, Speech-to-Text, Embeddings |
| **RAG** | Document upload, knowledge bases, web search, URL ingestion |
| **Agents** | Autonomous AI agents with tool use and long-running workflows |
| **MCP** | Full Model Context Protocol server support |
| **Admin** | RBAC, user management, groups, workspaces, usage analytics |
| **Deployment** | Docker, Railway, Kubernetes, bare metal |

---

## 🎯 Vision

To deliver a production-ready, enterprise AI workspace that teams and individuals can deploy in minutes — with every major AI provider available immediately upon configuration, zero vendor lock-in, and full data sovereignty.

---

## 💡 Mission

Make powerful AI accessible to every organization regardless of infrastructure preference. Provide a single, unified interface that grows with your team — from personal use to enterprise scale — while maintaining the security, privacy, and control your organization demands.

---

## 🔥 Highlights

- **Zero-config provider discovery** — set an API key, the provider appears automatically
- **Multi-key load balancing** — `OPENAI_API_KEY1`, `OPENAI_API_KEY2`, … spread load across keys
- **SHAHEEN-prefixed env aliases** — `SHAHEEN_SECRET_KEY`, `SHAHEEN_NAME`, `SHAHEEN_URL` for clean deployments
- **Google Search integration** — set `GOOGLE_SEARCH_API_KEY` + `GOOGLE_SEARCH_ENGINE_ID` to enable
- **Complete admin panel** — manage every aspect without touching source code
- **PWA** — installable progressive web app for desktop and mobile
- **Enterprise security** — RBAC, SSO/OAuth, encrypted secrets, audit logging

---

## ⭐ Features

- Multi-provider AI chat with simultaneous model access
- AI Agents with autonomous tool execution
- Retrieval-Augmented Generation (RAG) with document upload and knowledge bases
- MCP (Model Context Protocol) server connections
- Voice: ElevenLabs TTS, OpenAI TTS, Whisper STT
- Image generation: DALL-E, AUTOMATIC1111, ComfyUI
- Code interpreter with sandboxed Python execution
- Collaborative workspaces and shared knowledge bases
- Real-time streaming with WebSocket / Socket.IO
- Full i18n with 40+ languages
- Dark/light mode, customizable themes
- Aider AI coding assistant (optional, `ENABLE_AIDER=true`)

---

## 🧠 AI Capabilities

| Feature | Description |
|---|---|
| **Multi-model chat** | Switch models mid-conversation, compare responses |
| **System prompts** | Per-model, per-workspace, per-user system prompts |
| **Function calling** | Native tool / function calling support |
| **Vision** | Image understanding with GPT-4o, Claude, Gemini |
| **Long context** | 128K+ context windows supported |
| **Streaming** | Real-time token streaming for all providers |
| **Memory** | Persistent user memories and context |

---

## 🤖 Supported Models

| Provider | Auto-discovered | Key Variable |
|---|---|---|
| OpenAI (GPT-4o, o1, o3) | ✅ | `OPENAI_API_KEY` |
| Anthropic (Claude 3.5/3 series) | ✅ | `ANTHROPIC_API_KEY` |
| Google Gemini | ✅ | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Groq (LLaMA, Mixtral) | ✅ | `GROQ_API_KEY` |
| Mistral AI | ✅ | `MISTRAL_API_KEY` |
| xAI Grok | ✅ | `XAI_API_KEY` |
| DeepSeek | ✅ | `DEEPSEEK_API_KEY` |
| OpenRouter (100+ models) | ✅ | `OPENROUTER_API_KEY` |
| Ollama (local models) | ✅ optional | `OLLAMA_BASE_URL` |
| Azure OpenAI | ✅ | `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` |
| LM Studio / Any OpenAI-compatible | ✅ | `OPENAI_API_BASE_URLS` |

---

## 🔌 Integrations

- **Search**: Tavily, Exa, Bing, Google PSE, Brave, Perplexity, Firecrawl
- **Voice**: ElevenLabs, OpenAI TTS, Whisper
- **Storage**: AWS S3, Google Cloud Storage, Azure Blob
- **Database**: PostgreSQL, SQLite, MariaDB
- **Vector DB**: ChromaDB, pgvector, Qdrant, Milvus, OpenSearch
- **Auth**: OAuth2, LDAP, SAML (via proxy), API keys
- **GitHub**: Repository import, clone, edit, commit, push
- **Slack**: Bot integration via `SLACK_BOT_TOKEN`

---

## 🧩 Plugins

- Custom Python pipelines (filters, actions, providers)
- Tool functions with schema-driven UI
- MCP server connections (stdio + SSE transport)
- Workspace-scoped plugin assignments

---

## 🛠 Tools

Built-in tools available to AI agents:

- Web search (multiple providers)
- Web scraping / URL loader
- Code interpreter (sandboxed Python)
- File reader (PDF, DOCX, XLSX, CSV, images)
- Image generation
- GitHub operations

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────┐
│              SvelteKit Frontend             │
│     (TypeScript · Tailwind CSS · Vite)      │
└───────────────────┬─────────────────────────┘
                    │ HTTP / WebSocket / Socket.IO
┌───────────────────▼─────────────────────────┐
│              FastAPI Backend                │
│   (Python 3.11+ · Uvicorn · SQLAlchemy)     │
├─────────────────────────────────────────────┤
│  Routers: OpenAI · Ollama · Retrieval ·     │
│  Auths · Chats · Models · Tools · MCP       │
├─────────────────────────────────────────────┤
│  Database: PostgreSQL / SQLite (Alembic)    │
│  Vector DB: ChromaDB / pgvector / Qdrant    │
│  Cache: Redis (optional)                    │
└─────────────────────────────────────────────┘
```

---

## 📐 System Design

- **Stateless API layer** — horizontally scalable FastAPI workers
- **Event-driven** — Socket.IO for real-time chat streaming
- **Pluggable storage** — swap vector DB or file storage without code changes
- **Config-driven** — all features toggle-able via environment variables or admin UI
- **Multi-tenant** — RBAC with users, groups, workspaces, permissions

---

## 🔄 Workflow

1. User authenticates (local, OAuth, LDAP)
2. Selects model(s) from auto-discovered provider pool
3. Sends message → backend routes to provider
4. Response streams back via Socket.IO
5. Optional: RAG retrieval, tool execution, agent loop

---

## 📊 Performance

- Sub-100ms API response (excluding LLM latency)
- Streaming first-token in <500ms for most providers
- Concurrent user support via async FastAPI + Socket.IO
- Redis optional for session and cache scaling

---

## 🔐 Security

- JWT-based authentication with configurable expiry
- RBAC: admin, user, pending roles
- Encrypted valve/tool secrets (`ENABLE_VALVE_ENCRYPTION`)
- Cookie security: `SHAHEEN_SESSION_COOKIE_SECURE`, `WEBUI_SESSION_COOKIE_SECURE`
- OAuth2 / OIDC provider support
- LDAP integration

---

## 🛡 Privacy

- All data stored in your own database (no telemetry by default)
- Local model support via Ollama — no data leaves your infrastructure
- File uploads stored in your configured storage backend
- Session data encrypted at rest

---

## 🌐 Deployment

### ☁️ Cloud Deployment

**Railway (Recommended)**

1. Fork this repository
2. Connect to Railway
3. Set environment variables (see [Environment Variables](#-environment-variables))
4. Railway builds via `Dockerfile` and deploys automatically

**Docker**

```bash
docker run -d \
  -p 8080:8080 \
  -e WEBUI_NAME="SHAHEEN-YS-UI" \
  -e OPENAI_API_KEY="your-key" \
  -v shaheen-data:/app/backend/data \
  --name shaheen-ys-ui \
  --restart always \
  ghcr.io/open-webui/open-webui:latest
```

**Docker Compose**

```bash
cp .env.example .env
# Edit .env with your API keys
docker compose up -d
```

---

## 🖥 Self Hosting

```bash
# Clone the repo
git clone https://github.com/SHAHEEN-YS-UI/SHAHEEN--YS-UI
cd SHAHEEN--YS-UI

# Configure environment
cp .env.example .env
# Edit .env

# Start with Docker Compose
docker compose up -d

# Or start backend directly
cd backend && bash start.sh
```

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (recommended) or SQLite

### From Source

```bash
# Install Node dependencies and build frontend
npm install
npm run build

# Install Python dependencies
pip install -r backend/requirements.txt

# Start server
PORT=8080 bash backend/start.sh
```

---

## ⚙️ Configuration

All configuration is via environment variables. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

---

## 🔑 Environment Variables

### Core

| Variable | Description | Default |
|---|---|---|
| `WEBUI_NAME` / `SHAHEEN_NAME` | Application display name | `SHAHEEN-YS-UI` |
| `WEBUI_SECRET_KEY` / `SHAHEEN_SECRET_KEY` | JWT signing secret | auto-generated |
| `WEBUI_URL` / `SHAHEEN_URL` | Public URL of the deployment | `http://localhost:8080` |
| `DATABASE_URL` | PostgreSQL connection string | SQLite (local) |
| `PORT` | Server port | `8080` |

### AI Providers (auto-discovered)

| Variable | Provider | Notes |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI | Also: `OPENAI_API_KEY1`, `OPENAI_API_KEY2`, … |
| `ANTHROPIC_API_KEY` | Anthropic Claude | |
| `GEMINI_API_KEY` | Google Gemini | Also: `GOOGLE_API_KEY` |
| `GROQ_API_KEY` | Groq | Also: `GROQ_API_KEY1`, `GROQ_API_KEY2`, … |
| `MISTRAL_API_KEY` | Mistral AI | Also: `MISTRAL_API_KEY1`, … |
| `OPENROUTER_API_KEY` | OpenRouter | Also: `OPENROUTER_API_KEY1`, `OPENROUTER_API_KEY2`, … |
| `XAI_API_KEY` | xAI Grok | |
| `DEEPSEEK_API_KEY` | DeepSeek | |
| `OLLAMA_BASE_URL` | Ollama (local) | Optional |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI | Requires `AZURE_OPENAI_ENDPOINT` |

### Search & Tools

| Variable | Description |
|---|---|
| `GOOGLE_SEARCH_API_KEY` / `GOOGLE_PSE_API_KEY` | Google Programmable Search API key |
| `GOOGLE_SEARCH_ENGINE_ID` / `GOOGLE_PSE_ENGINE_ID` | Google Search Engine ID |
| `TAVILY_API_KEY` | Tavily web search |
| `EXA_API_KEY` | Exa search |
| `FIRECRAWL_API_KEY` | Firecrawl web scraper |
| `BRAVE_SEARCH_API_KEY` | Brave Search |

### Security & Sessions

| Variable | Alias | Description |
|---|---|---|
| `WEBUI_SESSION_COOKIE_SECURE` | `SHAHEEN_SESSION_COOKIE_SECURE` | Enable secure cookies (HTTPS) |
| `WEBUI_SESSION_COOKIE_SAME_SITE` | `SHAHEEN_SESSION_COOKIE_SAME_SITE` | Cookie SameSite policy |
| `ENABLE_VALVE_ENCRYPTION` | — | Encrypt tool/valve secrets at rest |

### Infrastructure

| Variable | Description |
|---|---|
| `REDIS_URL` | Redis for session/cache scaling |
| `VECTOR_DB` | Vector store: `chroma`, `pgvector`, `qdrant`, `milvus`, `opensearch` |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS |
| `SLACK_BOT_TOKEN` | Slack bot integration |
| `GITHUB_TOKEN` | GitHub API access |
| `ENABLE_AIDER` | Enable Aider AI coding assistant (`true`/`false`) |

See `.env.example` for the full list of 150+ configuration options.

---

## 💻 Development

### 🎨 Frontend Development

```bash
# Install dependencies
npm install

# Start Vite dev server
npm run dev

# Build for production
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

### ⚙️ Backend Development

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn open_webui.main:app --reload --port 8080

# Or use the start script
PORT=8080 bash start.sh
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend type checking
npm run check

# Linting
npm run lint
```

---

## ✅ Quality Assurance

- Static type checking: `mypy` (backend), `svelte-check` (frontend)
- Linting: `ruff` (Python), `ESLint` (TypeScript/Svelte)
- Code formatting: `black` (Python), `prettier` (frontend)
- CI/CD: GitHub Actions (lint, build, test, deploy)

---

## 📚 Documentation

- [Environment Variables Reference](.env.example)
- [API Documentation](#-api-documentation) — available at `/docs` when running
- [Security Policy](docs/SECURITY.md)
- [Changelog](CHANGELOG.md)

---

## 🔗 API Documentation

The FastAPI backend exposes interactive API docs at:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`
- **OpenAPI JSON**: `http://localhost:8080/openapi.json`

---

## 🗄 Database

| Database | Support | Notes |
|---|---|---|
| SQLite | ✅ Default | Zero-config local development |
| PostgreSQL | ✅ Recommended | Set `DATABASE_URL` |
| MariaDB | ✅ | Install `mariadb` extra |

Schema migrations are managed by Alembic and run automatically on startup.

---

## 🧠 Machine Learning Pipeline

1. **Document ingestion** — PDF, DOCX, XLSX, images, URLs
2. **Chunking** — configurable chunk size and overlap
3. **Embedding** — local (sentence-transformers) or API-based
4. **Vector storage** — ChromaDB, pgvector, Qdrant, Milvus, OpenSearch
5. **Retrieval** — semantic search + BM25 hybrid
6. **Reranking** — optional reranker model
7. **Generation** — augmented prompt to LLM

---

## 📁 Project Structure

```
SHAHEEN-YS-UI/
├── backend/
│   └── open_webui/
│       ├── main.py          # FastAPI application entry point
│       ├── config.py        # Environment configuration
│       ├── env.py           # Environment variables + SHAHEEN aliases
│       ├── models/          # Database ORM models
│       ├── routers/         # API route handlers
│       ├── retrieval/       # RAG pipeline
│       └── utils/           # Utilities (auth, telemetry, etc.)
├── src/
│   ├── app.html             # SvelteKit app shell
│   ├── routes/              # Page routes
│   └── lib/
│       ├── components/      # UI components
│       ├── stores/          # Svelte stores
│       └── apis/            # Backend API clients
├── static/                  # Static assets (favicon, logo, etc.)
├── backend/start.sh         # Production start script
├── Dockerfile               # Docker build
├── docker-compose.yaml      # Docker Compose stack
├── railway.toml             # Railway deployment config
└── pyproject.toml           # Python project + dependencies
```

---

## 🧬 Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | SvelteKit 5, TypeScript, Tailwind CSS 4, Vite |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, Alembic |
| **Real-time** | Socket.IO, WebSockets |
| **Database** | PostgreSQL / SQLite |
| **Vector DB** | ChromaDB, pgvector, Qdrant, Milvus |
| **AI SDKs** | openai, anthropic, google-genai, langchain |
| **Auth** | JWT, OAuth2, LDAP, Authlib |
| **Infra** | Docker, Railway, Redis |

---

## 🛠 Developer Tools

- `uv` — fast Python package management
- `ruff` — Python linting and formatting
- `svelte-check` — frontend type checking
- `alembic` — database migration management
- `hatchling` — Python build backend

---

## 🧰 Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.11 | 3.12 |
| Node.js | 20 | 20 LTS |
| RAM | 2 GB | 4 GB+ |
| Storage | 5 GB | 20 GB+ |
| CPU | 2 cores | 4+ cores |

---

## 📋 Prerequisites

- Git
- Python 3.11+ with pip
- Node.js 20+ with npm
- PostgreSQL (for production)
- Docker (for containerized deployment)

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/SHAHEEN-YS-UI/SHAHEEN--YS-UI
cd SHAHEEN--YS-UI

# 2. Configure
cp .env.example .env
# Set at minimum: OPENAI_API_KEY (or any provider key)

# 3. Run
docker compose up -d

# 4. Open
open http://localhost:8080
```

---

## 📝 Usage

1. Open the web interface at `http://localhost:8080`
2. Create an admin account on first launch
3. Navigate to **Admin → Connections** to review auto-discovered providers
4. Start a new chat and select any available model
5. Optionally: upload documents to knowledge bases for RAG

---

## 💬 Examples

**Chat with GPT-4o:**
> Select "gpt-4o" from the model dropdown and start chatting

**RAG with documents:**
> Upload a PDF → Ask questions about it in the chat

**Multi-model comparison:**
> Enable multiple models in chat settings to compare responses side-by-side

**Autonomous agent:**
> Create an Agent in the Workspace with web search + code interpreter tools enabled

---

## 🎨 Customization

- **Branding**: Set `WEBUI_NAME` / `SHAHEEN_NAME` and replace assets in `static/static/`
- **Theme**: Admin → Settings → Interface → Theme
- **System prompts**: Admin → Settings → Interface → Default System Prompt
- **Models**: Admin → Settings → Models — filter, alias, sort available models

---

## 🔧 Advanced Configuration

```bash
# Multiple API keys with load balancing
OPENAI_API_KEY=sk-primary
OPENAI_API_KEY1=sk-secondary
OPENAI_API_KEY2=sk-tertiary

# Multiple providers auto-registered
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
MISTRAL_API_KEY=...

# Google Programmable Search
GOOGLE_SEARCH_API_KEY=your-key
GOOGLE_SEARCH_ENGINE_ID=your-engine-id

# SHAHEEN aliases
SHAHEEN_SECRET_KEY=your-secret-key
SHAHEEN_NAME=My AI Hub
SHAHEEN_URL=https://ai.example.com
```

---

## 🧱 Building From Source

```bash
# 1. Install Node 20 and Python 3.12
# 2. Build frontend
npm install
NODE_OPTIONS="--max-old-space-size=4096" npm run build

# 3. Install Python deps
pip install -r backend/requirements.txt

# 4. Run
PORT=8080 bash backend/start.sh
```

---

## 🐳 Docker

```bash
# Build
docker build -t shaheen-ys-ui .

# Run
docker run -d -p 8080:8080 \
  -e OPENAI_API_KEY=sk-... \
  -v $(pwd)/backend/data:/app/backend/data \
  shaheen-ys-ui
```

---

## ☸️ Kubernetes

Basic deployment (see `deploy/` for full manifests):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shaheen-ys-ui
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: shaheen-ys-ui
        image: shaheen-ys-ui:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: shaheen-secrets
              key: DATABASE_URL
```

---

## ☁️ Infrastructure

Railway configuration is in `railway.toml`. The app is health-checked at `/health`.

Environment variables in Railway are set via the Railway dashboard. All keys listed in `.env.example` are supported.

---

## 🔄 CI/CD

GitHub Actions workflows (in `.github/workflows/`):

- **lint.yml** — ruff, eslint on every push
- **build.yml** — frontend build check
- **deploy.yml** — push to Railway on merge to main

---

## 🔁 Continuous Integration

Every pull request runs:
1. Python linting (ruff)
2. Frontend build verification
3. Type checking (svelte-check)
4. Backend unit tests

---

## 📈 Roadmap

- [ ] Multi-agent collaboration
- [ ] Voice call mode
- [ ] Enterprise SSO (SAML)
- [ ] Workflow automation builder
- [ ] Model fine-tuning interface
- [ ] Observability dashboard (OpenTelemetry)

---

## 🗓 Milestones

| Milestone | Status |
|---|---|
| Core platform (Open WebUI base) | ✅ Complete |
| SHAHEEN branding & aliases | ✅ Complete |
| Multi-provider auto-discovery | ✅ Complete |
| Multiple indexed API keys | ✅ Complete |
| Google Search integration | ✅ Complete |
| Railway deployment | ✅ Complete |
| Aider integration | ✅ Optional |
| Enterprise SSO | 🔄 Planned |

---

## 🚧 Current Status

**Production-ready.** Running on Railway and Replit with PostgreSQL backend.

---

## 🐛 Known Issues

- `chromadb>=1.0.0` is blocked by Replit's package firewall; `chromadb<1.0.0` (0.6.x) is used instead
- `accelerate` from the PyTorch CPU index conflicts with Python 3.12 resolution — installed from PyPI directly
- Aider cannot be installed on Replit (`litellm` blocked); set `ENABLE_AIDER=false`
- Frontend build requires `NODE_OPTIONS="--max-old-space-size=4096"` due to heap size

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

---

## 🔄 Migration Guide

Upgrading from Open WebUI:

1. All `WEBUI_*` environment variables continue to work unchanged
2. New `SHAHEEN_*` aliases are optional — existing deployments need no changes
3. Run `alembic upgrade head` if schema migrations are needed (handled automatically on startup)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'feat: add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow the existing code style (ruff for Python, prettier for frontend).

---

## 🧑‍💻 Contributors

Built on [Open WebUI](https://github.com/open-webui/open-webui) — thanks to the entire Open WebUI community.

SHAHEEN-YS-UI branding and enterprise extensions by the SHAHEEN-YS team.

---

## 💖 Sponsors

Want to sponsor SHAHEEN-YS-UI? Open an issue to discuss.

---

## 🌍 Community

- GitHub Issues — bug reports and feature requests
- GitHub Discussions — questions and ideas

---

## 💬 Discussions

Use [GitHub Discussions](https://github.com/SHAHEEN-YS-UI/SHAHEEN--YS-UI/discussions) for questions, ideas, and community conversation.

---

## 📢 Announcements

Watch the repository on GitHub for release announcements.

---

## 📜 License

This project is based on [Open WebUI](https://github.com/open-webui/open-webui).
Original work Copyright © Open WebUI Inc. — see [LICENSE](LICENSE) and [LICENSE_HISTORY](LICENSE_HISTORY).

SHAHEEN-YS-UI branding and modifications are applied on top of the upstream codebase.

---

## ⚖️ Legal

This software is provided under the MIT License. See [LICENSE](LICENSE) for full terms.

---

## 🙏 Acknowledgements

- [Open WebUI](https://github.com/open-webui/open-webui) — the powerful foundation this project is built on
- [FastAPI](https://fastapi.tiangolo.com) — high-performance Python API framework
- [SvelteKit](https://kit.svelte.dev) — modern full-stack web framework
- [LangChain](https://langchain.com) — LLM application framework
- All AI provider teams for their excellent APIs

---

## ⭐ Star History

If you find SHAHEEN-YS-UI useful, please ⭐ the repository!

---

## 📞 Contact

- GitHub Issues: [SHAHEEN-YS-UI/SHAHEEN--YS-UI](https://github.com/SHAHEEN-YS-UI/SHAHEEN--YS-UI/issues)

---

## 🔗 Links

- [GitHub Repository](https://github.com/SHAHEEN-YS-UI/SHAHEEN--YS-UI)
- [Open WebUI (upstream)](https://github.com/open-webui/open-webui)
- [Railway Deployment](https://railway.app)
- [FastAPI Docs](https://fastapi.tiangolo.com/docs)

---

## 🏆 Credits

| Role | Credit |
|---|---|
| Platform Foundation | Open WebUI Inc. |
| Enterprise Extensions | SHAHEEN-YS Team |
| AI Provider SDKs | OpenAI, Anthropic, Google, Groq, Mistral, xAI, DeepSeek |
| Infrastructure | Railway, Docker |

---

<div align="center">

Built with ❤️ on the Open WebUI platform

**SHAHEEN-YS-UI** — Enterprise AI, Your Way

</div>
