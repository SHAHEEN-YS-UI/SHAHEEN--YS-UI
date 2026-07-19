"""
SHAHEEN-YS-UI — Aider Integration
Optional built-in AI coding assistant powered by Aider.

Enable via environment variable:
    ENABLE_AIDER=true

Aider will automatically use whichever provider API keys are set:
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GROQ_API_KEY,
    MISTRAL_API_KEY, OPENROUTER_API_KEY, XAI_API_KEY, DEEPSEEK_API_KEY
"""

import os
import subprocess
import sys
from loguru import logger

ENABLE_AIDER = os.getenv('ENABLE_AIDER', 'false').lower() in ('true', '1', 'yes')


def _detect_aider_model() -> str | None:
    """Return the best available model for Aider based on configured API keys."""
    checks = [
        ('ANTHROPIC_API_KEY', 'claude-sonnet-4-5'),
        ('OPENAI_API_KEY', 'gpt-4o'),
        ('GEMINI_API_KEY', 'gemini/gemini-2.0-flash'),
        ('OPENROUTER_API_KEY', 'openrouter/anthropic/claude-3.5-sonnet'),
        ('GROQ_API_KEY', 'groq/llama-3.3-70b-versatile'),
        ('MISTRAL_API_KEY', 'mistral/mistral-large-latest'),
        ('XAI_API_KEY', 'xai/grok-2'),
        ('DEEPSEEK_API_KEY', 'deepseek/deepseek-chat'),
    ]
    for env_key, model in checks:
        if os.getenv(env_key):
            return model
    return None


def install_aider() -> bool:
    """Install Aider if not already available."""
    try:
        import aider  # noqa: F401
        return True
    except ImportError:
        logger.info('Aider not found — installing...')
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'aider-chat', '--quiet'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info('Aider installed successfully.')
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to install Aider: {e}')
            return False


def init_aider() -> dict:
    """
    Initialise Aider integration.
    Returns a status dict with keys: enabled, model, message.
    """
    if not ENABLE_AIDER:
        return {'enabled': False, 'model': None, 'message': 'Aider disabled (set ENABLE_AIDER=true to enable)'}

    if not install_aider():
        return {'enabled': False, 'model': None, 'message': 'Aider could not be installed'}

    model = _detect_aider_model()
    if not model:
        return {
            'enabled': False,
            'model': None,
            'message': 'Aider enabled but no provider API key detected. Set at least one of: '
                       'OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GROQ_API_KEY, '
                       'MISTRAL_API_KEY, OPENROUTER_API_KEY, XAI_API_KEY, DEEPSEEK_API_KEY',
        }

    logger.info(f'Aider integration active — using model: {model}')
    return {'enabled': True, 'model': model, 'message': f'Aider ready with model {model}'}


# Singleton status — evaluated once at import time when ENABLE_AIDER=true
_aider_status: dict | None = None


def get_aider_status() -> dict:
    global _aider_status
    if _aider_status is None:
        _aider_status = init_aider()
    return _aider_status
