# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>
from typing import Callable, Final, cast

from .base import LLMProvider
from .ollama import OllamaProvider
from .claude import ClaudeProvider
from .openai import OpenAIProvider

import ollama

ModelFactory = Callable[[str, str | None], LLMProvider]

openai_models: Final = (
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "o1",
    "o1-mini",
    "o1-preview",
)

claude_models: Final = (
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-sonnet-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
)


# Get available ollama models dynamically at runtime
try: 
    ollama_models = cast(list[str], [m.model for m in ollama.list().models])
except ConnectionError:
    ollama_models = []

models: dict[str, ModelFactory] = {
    **{model: OpenAIProvider for model in openai_models},
    **{model: ClaudeProvider for model in claude_models},
    **{model: OllamaProvider for model in ollama_models},
}

def create_model(model_name: str, api_key: str | None = None) -> LLMProvider:
    if model_name not in models:
        raise ValueError(f"Unknown model: {model_name!r}. Available: {list(models)}")
    return models[model_name](model_name, api_key)
