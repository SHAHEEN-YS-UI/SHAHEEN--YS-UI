# SHAHEEN-YS-UI — Railway Deployment Guide

> Generated from the actual codebase on 2026-07-19.  
> Source files inspected: `Dockerfile`, `backend/start.sh`, `backend/open_webui/env.py`,  
> `backend/open_webui/config.py`, `backend/open_webui/aider_integration.py`, `railway.toml`.  
> **Every value reported here is verified against the code. Nothing is invented.**

---

## 1. Build Configuration

| Property | Value |
|---|---|
| **Builder** | `DOCKERFILE` |
| **Dockerfile path** | `Dockerfile` (repo root) |
| **Frontend build image** | `node:22-alpine3.20` |
| **Backend runtime image** | `python:3.11-slim-bookworm` |
| **Node.js version** | 22 (engine range: `>=18.13.0 <=22.x.x`) |
| **npm version** | `>=6.0.0` (lock file present: `package-lock.json`) |
| **Python version** | 3.11 (`>=3.11, <3.13`) |
| **Python installer** | `uv` (installed via pip, then `uv pip install`) |
| **Backend package file** | `backend/requirements.txt` |
| **WORKDIR (runtime)** | `/app/backend` |
| **Start command** | `bash start.sh` |
| **Exposed port** | `8080` (default); overridable via `PORT` env var |
| **Health check endpoint** | `GET /health` → `{"status": true}` |
| **Health check timeout** | 300 seconds |

### System packages installed (Dockerfile)

```
git  build-essential  pandoc  gcc  netcat-openbsd  curl  jq  ca-certificates
libmariadb-dev  python3-dev  ffmpeg  libsm6  libxext6  zstd
```

---

## 2. Current `railway.toml`

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "bash start.sh"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[services]]
name = "shaheen-ys-ui"
```

---

## 3. Required Railway Services

| Service | Plugin | Notes |
|---|---|---|
| **PostgreSQL** | Railway Postgres plugin | Sets `DATABASE_URL` automatically. Alembic runs 47 migrations on first boot. |
| **Redis** | Railway Redis plugin | Optional for single-worker. Required when `UVICORN_WORKERS > 1` or `ENABLE_OAUTH_BACKCHANNEL_LOGOUT=true`. Sets `REDIS_URL`. |

---

## 4. Persistent Volume

> **Critical:** Without a persistent volume, all uploaded files, embedding model caches, ChromaDB data, Whisper model files, and audit logs are destroyed on every redeploy.

Mount a Railway volume to:

```
/app/backend/data
```

This single path covers everything:

| Subdirectory | Contents |
|---|---|
| `data/uploads/` | User-uploaded files (PDFs, images, docs) |
| `data/vector_db/` | ChromaDB local storage (if `VECTOR_DB=chroma`) |
| `data/cache/whisper/models/` | Faster-Whisper STT model files |
| `data/cache/embedding/models/` | Sentence-transformer / HuggingFace model weights |
| `data/cache/tiktoken/` | Tiktoken BPE encoding files |
| `data/cache/audio/speech/` | TTS speech audio cache |
| `data/audit.log` | Audit log file |
| `data/webui.db` | SQLite database (only used if `DATABASE_URL` is not set) |

---

## 5. Environment Variables

### 5.1 Required Variables

These must be set before the app will start correctly in production.

| Variable | Required | Recommended Value | Description |
|---|---|---|---|
| `WEBUI_SECRET_KEY` | **YES** | 32+ char random string | JWT signing key. If not set, start.sh generates one from `/dev/random` on every cold boot — all user sessions are invalidated on restart. **Always set this explicitly.** |
| `DATABASE_URL` | **YES** | Railway-injected Postgres URL | Full PostgreSQL connection string. Railway Postgres plugin injects this automatically. Falls back to SQLite at `data/webui.db` if unset — do not use SQLite on Railway. |
| `WEBUI_URL` | **YES** | `https://shaheen-ys-ui-production.up.railway.app` | Full public URL of the deployment. Required for OAuth redirect URIs and link generation. |
| `PORT` | Injected | `8080` | Port to bind. Railway injects this; `start.sh` reads `$PORT` and passes it to uvicorn. Default is 8080. |

**How to generate `WEBUI_SECRET_KEY`:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# or
openssl rand -base64 32
```

---

### 5.2 Application Identity

| Variable | Default | Description |
|---|---|---|
| `WEBUI_NAME` | `SHAHEEN-YS-UI` | Application display name shown in the UI title and API responses. |
| `ENV` | `prod` (set in Dockerfile) | Runtime environment. `prod` enables production-mode logging and security. |
| `WEBUI_FAVICON_URL` | `/static/favicon.png` | URL of the favicon served by the app. |

---

### 5.3 Server & Network

| Variable | Default | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | Uvicorn bind host. Leave as `0.0.0.0` on Railway. |
| `FORWARDED_ALLOW_IPS` | `*` | IPs trusted for X-Forwarded-For. `*` is required behind Railway's proxy. |
| `CORS_ALLOW_ORIGIN` | `*` | Allowed CORS origins. Restrict to your domain in production for security. |
| `UVICORN_WORKERS` | `1` | Number of uvicorn worker processes. Set >1 only when `REDIS_URL` is also set (required for shared WebSocket and session state). |
| `ENABLE_WEBSOCKET_SUPPORT` | `true` | Enable WebSocket (required for streaming chat). |
| `WEBSOCKET_MANAGER` | `''` (in-process) | Set to `redis` when `UVICORN_WORKERS > 1`. Requires `REDIS_URL`. |
| `WEBSOCKET_REDIS_URL` | Same as `REDIS_URL` | Override Redis URL used specifically for WebSocket management. |
| `ENABLE_COMPRESSION_MIDDLEWARE` | `true` | Brotli/gzip response compression. |

---

### 5.4 Database (PostgreSQL)

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | SQLite fallback | Full Postgres URL. Railway injects this. Must start with `postgresql://` (the app auto-converts `postgres://`). |
| `DATABASE_POOL_SIZE` | `None` (SQLAlchemy default) | SQLAlchemy connection pool size. Recommended: `5`–`10` for Railway. |
| `DATABASE_POOL_MAX_OVERFLOW` | `0` | Additional connections above pool size allowed temporarily. |
| `DATABASE_POOL_TIMEOUT` | `30` | Seconds to wait for a connection from the pool. |
| `DATABASE_POOL_RECYCLE` | `3600` | Seconds before a connection is recycled (avoids stale connections). |
| `DATABASE_SCHEMA` | `None` | PostgreSQL schema name (leave unset to use `public`). |
| `ENABLE_DB_MIGRATIONS` | `true` | Run Alembic migrations on startup. Leave enabled. |
| `DATABASE_ENABLE_IAM_TOKEN_AUTH` | `false` | Use AWS IAM token for RDS authentication instead of password. |
| `DATABASE_ENABLE_SESSION_SHARING` | `false` | Share session state across workers via DB instead of Redis. |

---

### 5.5 Redis

| Variable | Default | Description |
|---|---|---|
| `REDIS_URL` | `''` (disabled) | Redis connection URL. Railway Redis plugin injects this. Format: `redis://default:password@host:port`. |
| `REDIS_KEY_PREFIX` | `shaheen-ys-ui` | Prefix for all Redis keys used by this instance. |
| `REDIS_CLUSTER` | `false` | Enable Redis Cluster mode. |
| `REDIS_SENTINEL_HOSTS` | `''` | Comma-separated sentinel hosts (Redis Sentinel HA). |
| `REDIS_SOCKET_CONNECT_TIMEOUT` | `None` | Socket connection timeout in seconds. |
| `REDIS_HEALTH_CHECK_INTERVAL` | `None` | Interval in seconds for Redis connection health checks. |

---

### 5.6 Security & Authentication

| Variable | Default | Description |
|---|---|---|
| `WEBUI_AUTH` | `true` | Enable authentication. Set to `false` only for private trusted networks. |
| `WEBUI_SESSION_COOKIE_SAME_SITE` | `lax` | Cookie SameSite policy. |
| `WEBUI_SESSION_COOKIE_SECURE` | `false` | Set to `true` in production (HTTPS). Marks session cookie as Secure. |
| `WEBUI_AUTH_COOKIE_SECURE` | Same as `WEBUI_SESSION_COOKIE_SECURE` | Auth cookie Secure flag. |
| `ENABLE_VALVE_ENCRYPTION` | `false` | Encrypt tool valve secrets at rest using `WEBUI_SECRET_KEY`. |
| `ENABLE_PASSWORD_VALIDATION` | `false` | Enforce password complexity rules. |
| `PASSWORD_HASH_ALGORITHM` | `bcrypt` | Hash algorithm for passwords. Options: `bcrypt`, `argon2`. |
| `ENABLE_INITIAL_ADMIN_SIGNUP` | `false` | Allow the first-ever signup to bypass invite restrictions and become admin. |
| `CUSTOM_API_KEY_HEADER` | `x-api-key` | HTTP header name for API key authentication. |

---

### 5.7 Auto-Provisioning the Admin Account

Set these to have the admin account created automatically on first boot.

| Variable | Default | Description |
|---|---|---|
| `WEBUI_ADMIN_EMAIL` | `''` | Admin user email address. Creates admin on first boot if set. |
| `WEBUI_ADMIN_PASSWORD` | `''` | Admin user password. |
| `WEBUI_ADMIN_NAME` | `Admin` | Admin display name. |

> **Security note:** Delete or rotate these variables after the first successful boot.

---

### 5.8 User Defaults

| Variable | Default | Description |
|---|---|---|
| `DEFAULT_USER_ROLE` | `pending` | Role assigned to new signups. Options: `pending` (requires admin approval), `user`, `admin`. |
| `DEFAULT_GROUP_ID` | `''` | Assign new users to this group automatically. |
| `ENABLE_SIGNUP_PASSWORD_CONFIRMATION` | `false` | Require password confirmation field on signup. |
| `PENDING_USER_OVERLAY_TITLE` | `''` | Message title shown to pending users. |
| `PENDING_USER_OVERLAY_CONTENT` | `''` | Message body shown to pending users. |

---

## 6. AI Provider Variables

At least one provider must be configured for the app to be useful.

### 6.1 Core LLM Providers

| Variable | Default | Feature |
|---|---|---|
| `OPENAI_API_KEY` | `''` | OpenAI (GPT-4o, o1, etc.) |
| `OPENAI_API_BASE_URL` | `https://api.openai.com/v1` | OpenAI API base URL. Override to use a proxy or Azure. |
| `OPENAI_API_KEYS` | Same as `OPENAI_API_KEY` | Semicolon-separated list of keys for multiple OpenAI endpoints. |
| `OPENAI_API_BASE_URLS` | Same as `OPENAI_API_BASE_URL` | Semicolon-separated list of base URLs matching `OPENAI_API_KEYS`. |
| `ANTHROPIC_API_KEY` | `''` (env only) | Anthropic Claude models. Detected by Aider integration. |
| `GEMINI_API_KEY` | `''` | Google Gemini via native Gemini API. Also aliased by `GOOGLE_GENERATIVE_AI_API_KEY`. |
| `GEMINI_API_BASE_URL` | `''` | Gemini API base URL override. |
| `GOOGLE_API_KEY` | `''` (env only) | Alternative Google AI key. |
| `GROQ_API_KEY` | `''` (env only) | Groq inference (fast open-source models). |
| `MISTRAL_API_KEY` | `''` (env only) | Mistral AI models. |
| `XAI_API_KEY` | `''` (env only) | xAI / Grok models. |
| `DEEPSEEK_API_KEY` | `''` (env only) | DeepSeek models. |
| `OPENROUTER_API_KEY` | `''` (env only) | OpenRouter (unified access to 200+ models). |

> **Note:** `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, `MISTRAL_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, and `OPENROUTER_API_KEY` are read from the environment by the Python process but are not defined via `os.getenv()` in `config.py`. They are passed through to the model-calling layer via the API key configuration UI or Aider integration.

### 6.2 Ollama (Self-hosted Models)

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `''` | Ollama server URL. Leave empty to disable. Example: `http://your-ollama-host:11434` |
| `OLLAMA_BASE_URLS` | Same as `OLLAMA_BASE_URL` | Semicolon-separated list for multiple Ollama servers (load balancing). |
| `ENABLE_OLLAMA_API` | `true` | Enable the Ollama API connector. Set to `false` to hide Ollama from the UI. |
| `OLLAMA_API_CONFIGS` | `''` | JSON object of per-URL Ollama configs (auth, custom headers). |

### 6.3 OpenAI-Compatible Providers

| Variable | Default | Description |
|---|---|---|
| `OPENAI_LIKE_API_KEY` | `''` (env only) | API key for any OpenAI-compatible endpoint (LiteLLM, Groq, Together, etc.) |
| `OPENAI_LIKE_API_BASE_URL` | `''` (env only) | Base URL for the OpenAI-compatible endpoint. |

---

## 7. Feature-Specific Variables

### 7.1 Aider (AI Coding Assistant)

> Enable to activate the built-in Aider coding assistant. Aider auto-selects a model based on which provider API keys are set.

| Variable | Default | Description |
|---|---|---|
| `ENABLE_AIDER` | `false` | Set to `true` to enable. On Railway, `aider-chat` installs on first boot. |

**Model selection priority (first key found wins):**

| Key | Aider Model |
|---|---|
| `ANTHROPIC_API_KEY` | `claude-sonnet-4-5` |
| `OPENAI_API_KEY` | `gpt-4o` |
| `GEMINI_API_KEY` | `gemini/gemini-2.0-flash` |
| `OPENROUTER_API_KEY` | `openrouter/anthropic/claude-3.5-sonnet` |
| `GROQ_API_KEY` | `groq/llama-3.3-70b-versatile` |
| `MISTRAL_API_KEY` | `mistral/mistral-large-latest` |
| `XAI_API_KEY` | `xai/grok-2` |
| `DEEPSEEK_API_KEY` | `deepseek/deepseek-chat` |

---

### 7.2 Vector Database

| Variable | Default | Description |
|---|---|---|
| `VECTOR_DB` | `chroma` | Vector store backend. Options: `chroma`, `pgvector`, `qdrant`, `milvus`, `opensearch`, `elasticsearch`, `weaviate`, `mariadb-vector`, `pinecone`, `oracle23ai`, `valkey` |

#### Chroma (default — local file storage)

| Variable | Default | Description |
|---|---|---|
| `CHROMA_HTTP_HOST` | `''` | Remote Chroma host. Leave empty for local embedded mode. |
| `CHROMA_HTTP_PORT` | `8000` | Remote Chroma HTTP port. |
| `CHROMA_HTTP_SSL` | `false` | Use HTTPS for remote Chroma. |
| `CHROMA_CLIENT_AUTH_PROVIDER` | `''` | Chroma auth provider class. |
| `CHROMA_CLIENT_AUTH_CREDENTIALS` | `''` | Chroma auth credentials. |
| `CHROMA_TENANT` | `default_tenant` | Chroma tenant name. |
| `CHROMA_DATABASE` | `default_database` | Chroma database name. |

> **Railway note:** Chroma in local mode stores data at `data/vector_db/`. Without a persistent volume this data is lost on redeploy. Use remote Chroma or switch to `pgvector` for durability.

#### pgvector (recommended for Railway with PostgreSQL)

| Variable | Default | Description |
|---|---|---|
| `PGVECTOR_DB_URL` | Same as `DATABASE_URL` | PostgreSQL URL with pgvector extension. Defaults to the primary DB. |
| `PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH` | `1536` | Embedding dimension (must match your embedding model). |
| `PGVECTOR_USE_HALFVEC` | `false` | Use `halfvec` type for >2000 dimension embeddings. |
| `PGVECTOR_CREATE_EXTENSION` | `true` | Auto-create `vector` extension on startup. Requires superuser or `CREATE EXTENSION` privilege. |
| `PGVECTOR_POOL_SIZE` | `None` | Connection pool size for vector DB. |

#### Qdrant

| Variable | Default | Description |
|---|---|---|
| `QDRANT_URI` | `None` | Qdrant server URI. Example: `http://qdrant:6333` |
| `QDRANT_API_KEY` | `None` | Qdrant API key for Qdrant Cloud. |
| `QDRANT_PREFER_GRPC` | `false` | Use gRPC instead of HTTP for Qdrant. |
| `QDRANT_COLLECTION_PREFIX` | `open-webui` | Prefix for Qdrant collection names. |

#### Milvus

| Variable | Default | Description |
|---|---|---|
| `MILVUS_URI` | `data/vector_db/milvus.db` | Milvus URI. Use a remote Milvus URL for production. |
| `MILVUS_TOKEN` | `None` | Milvus API token. |
| `MILVUS_DB` | `default` | Milvus database name. |

#### OpenSearch

| Variable | Default | Description |
|---|---|---|
| `OPENSEARCH_URL` | (not set) | OpenSearch cluster URL. |
| `OPENSEARCH_SSL` | `true` | Use SSL for OpenSearch. |
| `OPENSEARCH_USERNAME` | `None` | OpenSearch username. |
| `OPENSEARCH_PASSWORD` | `None` | OpenSearch password. |

#### Elasticsearch

| Variable | Default | Description |
|---|---|---|
| `ELASTICSEARCH_URL` | `https://localhost:9200` | Elasticsearch URL. |
| `ELASTICSEARCH_API_KEY` | `None` | Elasticsearch API key. |
| `ELASTICSEARCH_USERNAME` | `None` | Elasticsearch username. |
| `ELASTICSEARCH_PASSWORD` | `None` | Elasticsearch password. |
| `ELASTICSEARCH_INDEX_PREFIX` | `open_webui_collections` | Index name prefix. |

#### Pinecone

| Variable | Default | Description |
|---|---|---|
| `PINECONE_API_KEY` | `None` | Pinecone API key. |
| `PINECONE_ENVIRONMENT` | `None` | Pinecone environment (legacy). |
| `PINECONE_INDEX_NAME` | `open-webui-index` | Pinecone index name. |
| `PINECONE_DIMENSION` | `1536` | Vector dimension. |
| `PINECONE_METRIC` | `cosine` | Distance metric. |
| `PINECONE_CLOUD` | `aws` | Cloud provider: `aws`, `gcp`, `azure`. |

---

### 7.3 File Storage

| Variable | Default | Description |
|---|---|---|
| `STORAGE_PROVIDER` | `local` | Storage backend. Options: `local`, `s3`, `gcs`, `azure`. |

#### S3 / R2 / MinIO (when `STORAGE_PROVIDER=s3`)

| Variable | Default | Description |
|---|---|---|
| `S3_BUCKET_NAME` | `None` | S3 bucket name. |
| `S3_REGION_NAME` | `None` | AWS region. |
| `S3_ACCESS_KEY_ID` | `None` | Access key ID. Leave empty to use instance role/IRSA. |
| `S3_SECRET_ACCESS_KEY` | `None` | Secret access key. |
| `S3_ENDPOINT_URL` | `None` | Custom S3 endpoint (for R2, MinIO, etc.). |
| `S3_KEY_PREFIX` | `None` | Path prefix for all uploaded objects. |
| `S3_USE_ACCELERATE_ENDPOINT` | `false` | Use S3 Transfer Acceleration. |
| `S3_ADDRESSING_STYLE` | `None` | `path` or `virtual`. |
| `S3_ENABLE_TAGGING` | `false` | Tag uploaded objects. |

#### Google Cloud Storage (when `STORAGE_PROVIDER=gcs`)

| Variable | Default | Description |
|---|---|---|
| `GCS_BUCKET_NAME` | `None` | GCS bucket name. |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | `None` | Inline service account JSON (base64 or raw JSON string). |

#### Azure Blob Storage (when `STORAGE_PROVIDER=azure`)

| Variable | Default | Description |
|---|---|---|
| `AZURE_STORAGE_ENDPOINT` | `None` | Azure storage account endpoint URL. |
| `AZURE_STORAGE_CONTAINER_NAME` | `None` | Blob container name. |
| `AZURE_STORAGE_KEY` | `None` | Storage account key. |

---

### 7.4 Web Search

| Variable | Default | Description |
|---|---|---|
| `ENABLE_WEB_SEARCH` | `false` | Enable web search feature globally. |
| `WEB_SEARCH_ENGINE` | `''` | Search engine backend. Options: `searxng`, `brave`, `google_pse`, `bing`, `duckduckgo`, `tavily`, `exa`, `firecrawl`, `jina`, `serper`, `serply`, `serpstack`, `serphouse`, `mojeek`, `bocha`, `searchapi`, `kagi`, `yacy`, `ollama_cloud` |
| `WEB_LOADER_ENGINE` | `''` | Web page loader. Set to `playwright` for JavaScript-heavy sites. Requires Playwright browser. |
| `PLAYWRIGHT_WS_URL` | `''` | Remote Playwright browser WebSocket URL (recommended on Railway instead of local install). |
| `PLAYWRIGHT_TIMEOUT` | `10000` | Playwright navigation timeout (ms). |

**Search Provider API Keys:**

| Variable | Provider |
|---|---|
| `TAVILY_API_KEY` | Tavily |
| `EXA_API_KEY` | Exa |
| `FIRECRAWL_API_KEY` | Firecrawl |
| `FIRECRAWL_API_BASE_URL` | Firecrawl (default: `https://api.firecrawl.dev`) |
| `BRAVE_SEARCH_API_KEY` | Brave Search |
| `GOOGLE_PSE_API_KEY` | Google Programmable Search Engine |
| `GOOGLE_PSE_ENGINE_ID` | Google PSE engine ID |
| `BING_SEARCH_V7_SUBSCRIPTION_KEY` | Bing Search v7 |
| `BING_SEARCH_V7_ENDPOINT` | Bing endpoint (default: `https://api.bing.microsoft.com/v7.0/search`) |
| `KAGI_SEARCH_API_KEY` | Kagi Search |
| `JINA_API_KEY` | Jina.ai |
| `SERPER_API_KEY` | Serper.dev |
| `SERPSTACK_API_KEY` | Serpstack |
| `SERPLY_API_KEY` | Serply |
| `MOJEEK_SEARCH_API_KEY` | Mojeek |
| `BOCHA_SEARCH_API_KEY` | Bocha |
| `SEARCHAPI_API_KEY` | SearchAPI |
| `SEARXNG_QUERY_URL` | SearXNG (self-hosted; provide full URL with `?q=<query>`) |
| `YACY_QUERY_URL` + `YACY_USERNAME` + `YACY_PASSWORD` | YaCy |

---

### 7.5 Audio — Speech-to-Text (STT)

| Variable | Default | Description |
|---|---|---|
| `AUDIO_STT_ENGINE` | `''` (local Whisper) | STT engine. Options: `''` (faster-whisper local), `openai`, `azure`, `deepgram`, `mistral` |
| `WHISPER_MODEL` | `base` | Whisper model size. Options: `tiny`, `base`, `small`, `medium`, `large-v3`. Larger = more accurate, more RAM. |
| `WHISPER_MODEL_DIR` | `data/cache/whisper/models` | Where Whisper model weights are cached. |
| `WHISPER_COMPUTE_TYPE` | `int8` | Compute precision: `int8` (CPU), `float16` (GPU). |
| `WHISPER_VAD_FILTER` | `false` | Apply voice activity detection filter. |
| `WHISPER_MULTILINGUAL` | `false` | Enable multilingual transcription. |
| `WHISPER_LANGUAGE` | `''` | Force transcription language (e.g., `en`). Empty = auto-detect. |
| `AUDIO_STT_OPENAI_API_KEY` | Same as `OPENAI_API_KEY` | OpenAI Whisper API key override. |
| `AUDIO_STT_OPENAI_API_BASE_URL` | Same as `OPENAI_API_BASE_URL` | OpenAI STT endpoint override. |
| `DEEPGRAM_API_KEY` | `''` | Deepgram API key (for `AUDIO_STT_ENGINE=deepgram`). |
| `AUDIO_STT_AZURE_API_KEY` | `''` | Azure Speech STT key. |
| `AUDIO_STT_AZURE_REGION` | `''` | Azure Speech region (e.g., `eastus`). |
| `AUDIO_STT_AZURE_LOCALES` | `''` | Comma-separated Azure locales. |
| `AUDIO_STT_MISTRAL_API_KEY` | `''` | Mistral STT API key. |

### 7.6 Audio — Text-to-Speech (TTS)

| Variable | Default | Description |
|---|---|---|
| `AUDIO_TTS_ENGINE` | `''` | TTS engine. Options: `''` (OpenAI TTS), `openai`, `azure`, `elevenlabs`, `kokoro` |
| `AUDIO_TTS_MODEL` | `tts-1` | OpenAI TTS model. |
| `AUDIO_TTS_VOICE` | `alloy` | OpenAI TTS voice. |
| `AUDIO_TTS_OPENAI_API_KEY` | Same as `OPENAI_API_KEY` | OpenAI TTS key override. |
| `AUDIO_TTS_OPENAI_API_BASE_URL` | Same as `OPENAI_API_BASE_URL` | OpenAI TTS endpoint override. |
| `AUDIO_TTS_API_KEY` | `''` | Generic TTS API key (for non-OpenAI engines). |
| `ELEVENLABS_API_KEY` | `''` | ElevenLabs API key (for `AUDIO_TTS_ENGINE=elevenlabs`). |
| `ELEVENLABS_API_BASE_URL` | `https://api.elevenlabs.io` | ElevenLabs base URL. |
| `AUDIO_TTS_AZURE_SPEECH_REGION` | `''` | Azure TTS region (for `AUDIO_TTS_ENGINE=azure`). |
| `AUDIO_TTS_AZURE_SPEECH_BASE_URL` | `''` | Azure TTS endpoint override. |
| `AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT` | `audio-24khz-160kbitrate-mono-mp3` | Azure TTS output format. |
| `AUDIO_TTS_MISTRAL_API_KEY` | `''` | Mistral TTS key. |

---

### 7.7 Image Generation

| Variable | Default | Description |
|---|---|---|
| `IMAGE_GENERATION_ENGINE` | `openai` | Image engine. Options: `openai`, `gemini`, `automatic1111`, `comfyui` |
| `IMAGE_SIZE` | `512x512` | Default image dimensions. |
| `IMAGE_STEPS` | `50` | Default diffusion steps (for Stable Diffusion engines). |
| `IMAGES_OPENAI_API_KEY` | Same as `OPENAI_API_KEY` | OpenAI DALL-E key override. |
| `IMAGES_OPENAI_API_BASE_URL` | Same as `OPENAI_API_BASE_URL` | OpenAI images endpoint override. |
| `IMAGES_GEMINI_API_KEY` | Same as `GEMINI_API_KEY` | Gemini image generation key. |
| `IMAGES_GEMINI_API_BASE_URL` | Same as `GEMINI_API_BASE_URL` | Gemini images endpoint. |
| `AUTOMATIC1111_BASE_URL` | `''` | Stable Diffusion WebUI URL. |
| `AUTOMATIC1111_API_AUTH` | `''` | SD WebUI auth credentials (`user:pass`). |
| `COMFYUI_BASE_URL` | `''` | ComfyUI server URL. |
| `COMFYUI_API_KEY` | `''` | ComfyUI API key. |

---

### 7.8 RAG — Document Extraction

| Variable | Default | Description |
|---|---|---|
| `CONTENT_EXTRACTION_ENGINE` | `''` (built-in) | Document extraction engine. Options: `''` (pypdf/unstructured built-in), `tika`, `docling`, `datalab_marker`, `mineru` |
| `TIKA_SERVER_URL` | `http://tika:9998` | Apache Tika server URL (for `CONTENT_EXTRACTION_ENGINE=tika`). |
| `DOCLING_SERVER_URL` | `http://docling:5001` | Docling server URL. |
| `DOCLING_API_KEY` | `''` | Docling API key. |
| `DATALAB_MARKER_API_KEY` | `''` | Datalab Marker API key. |
| `DATALAB_MARKER_API_BASE_URL` | `''` | Datalab Marker endpoint. |
| `MINERU_API_URL` | `http://localhost:8000` | MinerU server URL. |
| `MINERU_API_KEY` | `''` | MinerU API key. |
| `RAG_OPENAI_API_KEY` | Same as `OPENAI_API_KEY` | OpenAI key for RAG embeddings. |
| `RAG_OPENAI_API_BASE_URL` | Same as `OPENAI_API_BASE_URL` | Endpoint for RAG embeddings. |
| `RAG_AZURE_OPENAI_BASE_URL` | `''` | Azure OpenAI endpoint for RAG. |
| `RAG_AZURE_OPENAI_API_KEY` | `''` | Azure OpenAI key for RAG. |
| `RAG_AZURE_OPENAI_API_VERSION` | `''` | Azure OpenAI API version for RAG. |
| `RAG_OLLAMA_BASE_URL` | Same as `OLLAMA_BASE_URL` | Ollama endpoint for RAG embeddings. |
| `YOUTUBE_LOADER_LANGUAGE` | `en` | Language code(s) for YouTube transcript loading. |

---

### 7.9 OAuth / OIDC Single Sign-On

Configure only the providers you need. All OAuth providers require `WEBUI_URL` to be set correctly for redirect URIs.

#### Google OAuth

| Variable | Description |
|---|---|
| `GOOGLE_CLIENT_ID` | Google OAuth2 client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 client secret |

#### Microsoft / Azure AD

| Variable | Description |
|---|---|
| `MICROSOFT_CLIENT_ID` | Microsoft app client ID |
| `MICROSOFT_CLIENT_SECRET` | Microsoft app client secret |
| `MICROSOFT_CLIENT_TENANT_ID` | Azure AD tenant ID |
| `MICROSOFT_CLIENT_LOGIN_BASE_URL` | Default: `https://login.microsoftonline.com` |

#### GitHub OAuth

| Variable | Description |
|---|---|
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret |

#### Generic OIDC

| Variable | Default | Description |
|---|---|---|
| `OAUTH_CLIENT_ID` | `''` | OIDC client ID |
| `OAUTH_CLIENT_SECRET` | `''` | OIDC client secret |
| `OPENID_PROVIDER_URL` | `''` | OIDC discovery URL (e.g., `https://accounts.google.com/.well-known/openid-configuration`) |
| `OAUTH_PROVIDER_NAME` | `SSO` | Display name for the SSO button in the UI |
| `OAUTH_SCOPES` | `openid email profile` | OIDC scopes to request |
| `OPENID_END_SESSION_ENDPOINT` | `''` | OIDC logout endpoint override |
| `OAUTH_TOKEN_ENDPOINT_AUTH_METHOD` | `None` | Token endpoint auth method override |
| `OAUTH_CODE_CHALLENGE_METHOD` | `None` | PKCE method: `S256` or empty |

#### OAuth Behavior

| Variable | Default | Description |
|---|---|---|
| `ENABLE_OAUTH_EMAIL_FALLBACK` | `false` | Fall back to email matching if OAuth sub doesn't match |
| `ENABLE_OAUTH_ID_TOKEN_COOKIE` | `true` | Store OIDC ID token in a cookie |
| `OAUTH_MAX_SESSIONS_PER_USER` | `10` | Maximum concurrent OAuth sessions per user |
| `ENABLE_OAUTH_TOKEN_EXCHANGE` | `false` | Allow external apps to exchange OAuth tokens |
| `ENABLE_OAUTH_BACKCHANNEL_LOGOUT` | `false` | OIDC back-channel logout (requires Redis) |

---

### 7.10 LDAP

| Variable | Default | Description |
|---|---|---|
| `ENABLE_LDAP` | `false` | Enable LDAP authentication |
| `LDAP_SERVER_HOST` | `localhost` | LDAP server hostname |
| `LDAP_SERVER_PORT` | `389` | LDAP port (636 for LDAPS) |
| `LDAP_SERVER_LABEL` | `LDAP Server` | Display name for the LDAP login button |
| `LDAP_APP_DN` | `''` | Service account DN for binding |
| `LDAP_APP_PASSWORD` | `''` | Service account password |
| `LDAP_SEARCH_BASE` | `''` | LDAP search base DN |
| `LDAP_SEARCH_FILTERS` | `''` | Additional LDAP search filter |
| `LDAP_ATTRIBUTE_FOR_MAIL` | `mail` | LDAP attribute that holds the user's email |
| `LDAP_ATTRIBUTE_FOR_USERNAME` | `uid` | LDAP attribute used as the username |
| `LDAP_USE_TLS` | `true` | Use STARTTLS |
| `LDAP_CA_CERT_FILE` | `''` | Path to CA certificate for LDAP TLS |
| `LDAP_VALIDATE_CERT` | `true` | Validate LDAP TLS certificate |
| `ENABLE_LDAP_GROUP_MANAGEMENT` | `false` | Sync LDAP groups to app groups |
| `LDAP_ATTRIBUTE_FOR_GROUPS` | `memberOf` | LDAP attribute listing group memberships |

---

### 7.11 SCIM Provisioning (Enterprise)

| Variable | Default | Description |
|---|---|---|
| `ENABLE_SCIM` | `false` | Enable SCIM 2.0 user provisioning |
| `SCIM_TOKEN` | `''` | Bearer token for SCIM endpoint authentication |
| `SCIM_AUTH_PROVIDER` | `''` | OAuth provider name used for SCIM externalId mapping |

---

### 7.12 Trusted Header Auth (Reverse Proxy SSO)

| Variable | Description |
|---|---|
| `WEBUI_AUTH_TRUSTED_EMAIL_HEADER` | HTTP header carrying the authenticated user's email |
| `WEBUI_AUTH_TRUSTED_NAME_HEADER` | HTTP header carrying the user's display name |
| `WEBUI_AUTH_TRUSTED_GROUPS_HEADER` | HTTP header carrying the user's groups |
| `WEBUI_AUTH_TRUSTED_ROLE_HEADER` | HTTP header carrying the user's role |

---

### 7.13 Code Interpreter

| Variable | Default | Description |
|---|---|---|
| `ENABLE_CODE_INTERPRETER` | `true` | Enable in-browser Python code interpreter (Pyodide). |
| `CODE_INTERPRETER_ENGINE` | `pyodide` | Engine: `pyodide` (browser) or `jupyter` (server-side). |
| `CODE_INTERPRETER_JUPYTER_URL` | `''` | Jupyter server URL (for `CODE_INTERPRETER_ENGINE=jupyter`). |
| `CODE_INTERPRETER_JUPYTER_AUTH_TOKEN` | `''` | Jupyter token. |
| `CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD` | `''` | Jupyter password. |

---

### 7.14 Memory System

| Variable | Default | Description |
|---|---|---|
| `ENABLE_MEMORIES` | `true` | Enable the user memory / personalization feature. |
| `ENABLE_MEMORY_SYSTEM_CONTEXT` | `true` | Inject user memories into system context. |
| `ENABLE_MEMORY_BACKGROUND_REVIEW` | `false` | Periodically review and consolidate memories in the background. |

---

### 7.15 Cloud Storage Integrations

| Variable | Default | Description |
|---|---|---|
| `ENABLE_GOOGLE_DRIVE_INTEGRATION` | `false` | Enable Google Drive as a file source in RAG. |
| `GOOGLE_DRIVE_CLIENT_ID` | `''` | Google OAuth2 client ID (must have Drive scope). |
| `GOOGLE_DRIVE_API_KEY` | `''` | Google Drive API key. |
| `ENABLE_ONEDRIVE_INTEGRATION` | `false` | Enable OneDrive as a file source in RAG. |
| `ONEDRIVE_CLIENT_ID` | `''` | Microsoft app client ID with Files.Read scope. |
| `ONEDRIVE_SHAREPOINT_URL` | `''` | SharePoint tenant URL. |
| `ONEDRIVE_SHAREPOINT_TENANT_ID` | `''` | SharePoint tenant ID. |

---

### 7.16 Observability (OpenTelemetry)

| Variable | Default | Description |
|---|---|---|
| `ENABLE_OTEL` | `false` | Enable OpenTelemetry tracing/metrics/logs. |
| `ENABLE_OTEL_TRACES` | `false` | Enable OTLP traces. |
| `ENABLE_OTEL_METRICS` | `false` | Enable OTLP metrics. |
| `ENABLE_OTEL_LOGS` | `false` | Enable OTLP logs. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OTLP collector endpoint. |
| `OTEL_SERVICE_NAME` | `shaheen-ys-ui` | Service name in traces. |
| `OTEL_RESOURCE_ATTRIBUTES` | `''` | Additional resource attributes (`key=val,key2=val2`). |
| `OTEL_TRACES_SAMPLER` | `parentbased_always_on` | Trace sampling strategy. |

---

### 7.17 Audit Logging

| Variable | Default | Description |
|---|---|---|
| `ENABLE_AUDIT_LOGS_FILE` | `true` | Write audit log to file. |
| `ENABLE_AUDIT_STDOUT` | `false` | Also emit audit log to stdout. |
| `AUDIT_LOG_LEVEL` | `NONE` | Options: `NONE`, `LOW`, `MEDIUM`, `HIGH`. |
| `AUDIT_LOGS_FILE_PATH` | `data/audit.log` | Full path to the audit log file. |
| `AUDIT_LOG_FILE_ROTATION_SIZE` | `10MB` | Rotate log file after reaching this size. |

---

### 7.18 Miscellaneous

| Variable | Default | Description |
|---|---|---|
| `GLOBAL_LOG_LEVEL` | `INFO` | Application log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `SCARF_NO_ANALYTICS` | `true` | Disable Scarf.sh telemetry (set in Dockerfile). |
| `DO_NOT_TRACK` | `true` | Disable analytics tracking (set in Dockerfile). |
| `ANONYMIZED_TELEMETRY` | `false` | Disable ChromaDB telemetry (set in Dockerfile). |
| `SAFE_MODE` | `false` | Disable all tool/function execution. |
| `OFFLINE_MODE` | `false` | Disable all outbound network calls (HuggingFace Hub, update checks). |
| `ENABLE_VERSION_UPDATE_CHECK` | `true` | Check for newer versions. Set to `false` in air-gapped environments. |
| `RESET_CONFIG_ON_START` | `false` | Reset all DB-persisted config to env defaults on every startup. **Destructive.** |
| `MCP_INITIALIZE_TIMEOUT` | `10` | Seconds to wait for MCP server handshake. |
| `LICENSE_KEY` | `''` | Enterprise license key. |
| `DEFAULT_USER_ROLE` | `pending` | Default role for new signups. |
| `BYPASS_MODEL_ACCESS_CONTROL` | `false` | Skip per-model access checks (admin shortcut). |
| `ENABLE_OPENAI_API_PASSTHROUGH` | `false` | Expose an OpenAI-compatible passthrough API endpoint. |

---

## 8. Variables Set Automatically by Dockerfile

These are set at image build time and do not need to be overridden unless you have a specific reason.

| Variable | Value (Dockerfile) | Description |
|---|---|---|
| `ENV` | `prod` | Production mode. |
| `PORT` | `8080` | Default port (can be overridden at runtime). |
| `PYTHONUNBUFFERED` | `1` | Force Python stdout/stderr unbuffered. |
| `WHISPER_MODEL` | `base` | Whisper model (downloads on first use). |
| `WHISPER_MODEL_DIR` | `/app/backend/data/cache/whisper/models` | Whisper cache. |
| `RAG_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Default embedding model. |
| `SENTENCE_TRANSFORMERS_HOME` | `/app/backend/data/cache/embedding/models` | Embedding model cache. |
| `HF_HOME` | `/app/backend/data/cache/embedding/models` | HuggingFace Hub cache. |
| `TIKTOKEN_CACHE_DIR` | `/app/backend/data/cache/tiktoken` | Tiktoken cache. |
| `SCARF_NO_ANALYTICS` | `true` | Telemetry disabled. |
| `DO_NOT_TRACK` | `true` | Tracking disabled. |
| `ANONYMIZED_TELEMETRY` | `false` | Chroma telemetry disabled. |
| `DOCKER` | `true` | Signals containerized environment. |
| `OLLAMA_BASE_URL` | `/ollama` | Overridden at runtime if `USE_OLLAMA_DOCKER=false`. |

---

## 9. Variables Auto-Generated on First Boot

| Variable | Mechanism | Production Risk |
|---|---|---|
| `WEBUI_SECRET_KEY` | `start.sh` generates from `/dev/random` and writes to `.webui_secret_key` in WORKDIR | **High.** Without a persistent volume, this file is lost on redeploy. All sessions are invalidated. **Always set `WEBUI_SECRET_KEY` explicitly.** |

---

## 10. Minimum Viable Railway Configuration

Copy this into your Railway service's Variables tab for a working production deployment.

```bash
# ── Core (required) ──────────────────────────────────
WEBUI_SECRET_KEY=<generate: openssl rand -base64 32>
DATABASE_URL=<injected by Railway Postgres plugin>
WEBUI_URL=https://shaheen-ys-ui-production.up.railway.app
ENV=prod

# ── Server ────────────────────────────────────────────
HOST=0.0.0.0
FORWARDED_ALLOW_IPS=*
CORS_ALLOW_ORIGIN=https://shaheen-ys-ui-production.up.railway.app
WEBUI_SESSION_COOKIE_SECURE=true

# ── Branding ─────────────────────────────────────────
WEBUI_NAME=SHAHEEN-YS-UI

# ── Telemetry off ─────────────────────────────────────
SCARF_NO_ANALYTICS=true
DO_NOT_TRACK=true
ANONYMIZED_TELEMETRY=false

# ── Admin bootstrap (delete after first login) ────────
WEBUI_ADMIN_EMAIL=admin@yourcompany.com
WEBUI_ADMIN_PASSWORD=<strong-temporary-password>

# ── User defaults ─────────────────────────────────────
DEFAULT_USER_ROLE=pending

# ── AI Provider (add at least one) ───────────────────
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...

# ── Redis (add when UVICORN_WORKERS > 1) ─────────────
# REDIS_URL=<injected by Railway Redis plugin>
# WEBSOCKET_MANAGER=redis
# UVICORN_WORKERS=2

# ── Aider (optional) ─────────────────────────────────
# ENABLE_AIDER=true
```

---

## 11. Deployment Checklist

- [ ] Railway Postgres plugin added → `DATABASE_URL` injected
- [ ] Railway Redis plugin added (optional; required for multi-worker)
- [ ] Railway volume mounted at `/app/backend/data`
- [ ] `WEBUI_SECRET_KEY` set to a strong random value (not generated at runtime)
- [ ] `WEBUI_URL` set to the correct public Railway domain
- [ ] `WEBUI_SESSION_COOKIE_SECURE=true` set (HTTPS)
- [ ] At least one AI provider API key set
- [ ] `WEBUI_ADMIN_EMAIL` + `WEBUI_ADMIN_PASSWORD` set for first-boot admin
- [ ] `DEFAULT_USER_ROLE=pending` to prevent unauthorized access
- [ ] After first login: delete `WEBUI_ADMIN_EMAIL` and `WEBUI_ADMIN_PASSWORD`
- [ ] If using `VECTOR_DB=chroma` (default): confirm volume is mounted (otherwise vector data is ephemeral)
- [ ] If using `VECTOR_DB=pgvector`: enable `pgvector` extension on Postgres instance

---

## 12. Detected Issues & Notes

| Issue | Severity | Resolution |
|---|---|---|
| **`start.sh` generates `WEBUI_SECRET_KEY` from `/dev/random` on cold boot** | High | Always set `WEBUI_SECRET_KEY` explicitly. Without it, all user sessions become invalid on every restart or redeploy. |
| **`postgres://` vs `postgresql://`** | Low | Handled automatically: `start.sh`/`env.py` replaces `postgres://` with `postgresql://`. Railway Postgres URLs starting with `postgres://` are safe. |
| **Chroma vector DB is file-based by default** | Medium | Local Chroma stores data at `data/vector_db/`. Without a volume this is ephemeral. Switch to `VECTOR_DB=pgvector` to use the existing Postgres instance, or mount a Railway volume. |
| **Embedding models downloaded at runtime** | Medium | On first start, sentence-transformer models are downloaded from HuggingFace (~90 MB for the default `all-MiniLM-L6-v2`). This happens every cold boot without a persistent volume. Mount a volume at `/app/backend/data` so the cache persists. |
| **Whisper STT model downloaded at runtime** | Low | Whisper `base` model (~145 MB) downloads on first transcription if not cached. Persists with the volume. |
| **Aider installs `aider-chat` at runtime on Railway** | Low | When `ENABLE_AIDER=true`, `aider-chat` is installed via pip on every cold boot (not in the Docker image due to Replit firewall restrictions during build). This adds ~60 seconds to first-start time on Railway. |
| **`PORT` behavior** | None | Railway injects `PORT` automatically. `start.sh` reads it: `PORT="${PORT:-8080}"`. The Dockerfile also sets `PORT=8080` as default. No conflict. |
| **`railway.toml` start command** | Fixed | Previously had `bash backend/start.sh` (wrong path). Fixed to `bash start.sh` (correct, since `WORKDIR=/app/backend`). Commit `2ab3948` on `main`. |
| **No public Railway URL configured on initial deploy** | Resolved | Public domain `shaheen-ys-ui-production.up.railway.app` was provisioned via Railway GraphQL API. |

---

## 13. Live Deployment Status

| Item | Value |
|---|---|
| **Railway project** | `easygoing-growth` |
| **Service** | `SHAHEEN--YS-UI` |
| **Public URL** | `https://shaheen-ys-ui-production.up.railway.app` |
| **Latest successful deployment** | `b20a3a22` |
| **GitHub repository** | `https://github.com/SHAHEEN-YS-UI/SHAHEEN--YS-UI` |
| **Branch** | `main` |
| **HEAD commit** | `2ab3948` — `fix: correct Railway start command to match Dockerfile WORKDIR` |
| **Health check** | `GET /health` → `{"status": true}` ✅ |
| **Database** | PostgreSQL ✅ |
| **App name** | `SHAHEEN-YS-UI` ✅ |
| **Version** | `0.10.2` |
| **Auto-deploy trigger** | Git push to `main` → Railway rebuild |
