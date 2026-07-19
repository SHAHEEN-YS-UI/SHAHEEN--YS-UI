# SHAHEEN-YS-UI

A modern self-hosted AI workspace supporting multiple AI providers through one unified interface — AI agents, MCP servers, tools, workflows, RAG, and enterprise deployment.

Built on the Open WebUI platform, SHAHEEN-YS-UI brings together every major AI provider and local model runner under a single, professionally branded interface deployable to Railway, Docker, or any cloud environment.

---

## Features

- **Multi-Provider AI** — OpenAI, Anthropic, Google Gemini, Groq, Mistral, xAI, DeepSeek, OpenRouter, Ollama, Azure OpenAI, LM Studio, and any OpenAI-compatible API, simultaneously
- **AI Agents** — Build and deploy autonomous agents with tool use and long-running workflows
- **RAG & Knowledge** — Upload documents, connect knowledge bases, and chat with your data
- **MCP Support** — Connect external tools via Model Context Protocol servers
- **Voice & Audio** — Text-to-speech and speech-to-text including ElevenLabs integration
- **Image Generation** — AUTOMATIC1111 / ComfyUI / DALL-E support
- **Pipelines** — Extend with custom Python functions and filters
- **Admin Dashboard** — Full user management, RBAC, groups, and usage analytics
- **PWA** — Installable progressive web app for desktop and mobile
- **Aider** — Optional built-in AI coding assistant (set `ENABLE_AIDER=true`)

---

## Quick Start

### Docker (Recommended)

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

### Docker Compose

```bash
cp .env.example .env
# Edit .env with your API keys
docker compose up -d
```

### Python (pip)

```bash
pip install open-webui
open-webui serve
```

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description |
|---|---|
| `WEBUI_NAME` | Application display name (default: `SHAHEEN-YS-UI`) |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GROQ_API_KEY` | Groq API key |
| `MISTRAL_API_KEY` | Mistral API key |
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `XAI_API_KEY` | xAI / Grok API key |
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `OLLAMA_BASE_URL` | Ollama instance URL (default: `http://localhost:11434`) |
| `DATABASE_URL` | PostgreSQL connection string (Railway / production) |
| `ENABLE_AIDER` | Enable Aider coding assistant (`true`/`false`) |
| `TAVILY_API_KEY` | Tavily web search key |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS key |

See `.env.example` for the full list.

---

## Railway Deployment

This project is pre-configured for Railway deployment.

1. Push to GitHub
2. Connect the repository to Railway
3. Set environment variables in the Railway dashboard (all keys from `.env.example`)
4. Railway will build via `Dockerfile` and deploy automatically

The `railway.toml` in this repository handles build, start command, and health check configuration.

---

## AI Providers

SHAHEEN-YS-UI automatically detects and enables any provider for which an API key is set. No code changes are needed to switch providers.

| Provider | Environment Variable |
|---|---|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` / `GOOGLE_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| xAI / Grok | `XAI_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Ollama | `OLLAMA_BASE_URL` |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` |

---

## Aider Integration

SHAHEEN-YS-UI ships with optional [Aider](https://aider.chat) support — an AI pair programming assistant in your terminal.

Enable it:
```bash
ENABLE_AIDER=true
```

Aider automatically picks up whichever provider API keys are available. No additional configuration required.

---

## License

This project is based on [Open WebUI](https://github.com/open-webui/open-webui).  
Original work Copyright © Open WebUI Inc. — see [LICENSE](./LICENSE) and [LICENSE_HISTORY](./LICENSE_HISTORY).

SHAHEEN-YS-UI branding and modifications are applied on top of the upstream codebase.
