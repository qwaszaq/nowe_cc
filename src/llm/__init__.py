"""
Local LLM Integration Module

Provides interface to local LM Studio server running openai/gpt-oss-20b
at 192.168.200.226
"""

from .local_client import LocalLLMClient, get_llm_client
from .agent_prompts import (
    MARCUS_SYSTEM_PROMPT,
    ADRIAN_SYSTEM_PROMPT,
    SOFIA_SYSTEM_PROMPT,
    MAYA_SYSTEM_PROMPT,
    LUCAS_SYSTEM_PROMPT,
    DAMIAN_SYSTEM_PROMPT,
    VIKTOR_SYSTEM_PROMPT,
    ELENA_SYSTEM_PROMPT,
    ALEX_SYSTEM_PROMPT
)

__all__ = [
    'LocalLLMClient',
    'get_llm_client',
    'MARCUS_SYSTEM_PROMPT',
    'ADRIAN_SYSTEM_PROMPT',
    'SOFIA_SYSTEM_PROMPT',
    'MAYA_SYSTEM_PROMPT',
    'LUCAS_SYSTEM_PROMPT',
    'DAMIAN_SYSTEM_PROMPT',
    'VIKTOR_SYSTEM_PROMPT',
    'ELENA_SYSTEM_PROMPT',
    'ALEX_SYSTEM_PROMPT'
]
