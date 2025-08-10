from typing import Callable
from .base import LLMProvider
from .openai import OpenAIProvider

ModelFactory = Callable[[str], LLMProvider]

openai_models = [
    "gpt-5",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "o1",
    "o1-mini",
    "o1-preview",
]

models: dict[str, ModelFactory] = {model: OpenAIProvider for model in openai_models}

def create_model(model_name: str) -> LLMProvider:
    if model_name not in models:
        raise ValueError(f"Unknown model: {model_name!r}. Available: {list(models)}")
    return models[model_name](model_name)
