---
name: SHAHEEN-YS-UI build & run setup
description: How to build and run SHAHEEN-YS-UI (Open WebUI fork) on Replit — Node version, blocked packages, and startup chain.
---

## Node.js version
- Requires **Node.js 20** (Node 18 too old for @shikijs/core ≥4.0)
- Install via: `installProgrammingLanguage({ language: "nodejs-20" })`
- Frontend build needs: `NODE_OPTIONS="--max-old-space-size=4096" npm run build`

**Why:** @shikijs/core@4.x (syntax highlighting) hard-requires Node ≥20. Node 18 shipped by default.

## Security-firewall-blocked npm packages
- `vitest` (all versions blocked) — remove from devDependencies; not needed for build/run
- Replace script: `"test:frontend": "echo 'vitest not installed'"`

## Security-firewall-blocked Python packages
- `chromadb==1.5.9` (blocked) — install `chromadb<1.0.0` (0.6.3 works)
- `litellm` / `aider-chat` (blocked) — Aider cannot be pip-installed in Replit; ENABLE_AIDER stays false

## Python packages needed beyond pyproject.toml pip install
psycopg2-binary, pgvector, typer, ldap3, opencv-python-headless,
sentence-transformers, faster-whisper, pypandoc, msoffcrypto-tool, pyxlsb, xlrd,
sentencepiece, soundfile, azure-ai-documentintelligence, azure-identity,
azure-storage-blob, google-api-python-client, google-auth-httplib2,
google-auth-oauthlib, googleapis-common-protos, google-cloud-storage,
boto3, pyarrow, python-slugify, python-magic, accelerate, einops,
opensearch-py, rapidocr-onnxruntime

**Why:** pyproject.toml pip install fails because hatch build hook runs npm install (which fails on Node 18). After Node 20, install deps individually in batches.

## Workflow command
`PORT=5000 WEBUI_NAME='SHAHEEN-YS-UI' bash backend/start.sh`
- Must use PORT=5000 for Replit webview output type
- start.sh CDs into backend/ before running uvicorn
- Auto-generates WEBUI_SECRET_KEY if not set via env

## Database
- DATABASE_URL (Railway PostgreSQL) connects successfully on startup
- All Alembic migrations run automatically on first start
- Uses psycopg2-binary for sync engine, psycopg (v3) for async engine

## Startup sequence (first run)
1. Secret key generated/loaded from .webui_secret_key
2. PostgreSQL connection + Alembic migrations
3. sentence-transformers/all-MiniLM-L6-v2 model downloaded (~931MB, first run only; cached after)
4. Server starts, Aider integration status logged
5. Health check at /health returns {"status": true}

## Verified working
- GET /health → {"status": true}
- GET /health/db → {"status": true}
- GET /api/config → name: "SHAHEEN-YS-UI", version: "0.10.2"
