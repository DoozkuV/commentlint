# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>
from typing import override
from anthropic import Anthropic

from commentlint.config import MAX_TOKENS

from .base import LLMProvider

class ClaudeProvider(LLMProvider):
    provider: str = "Anthropic"
    env_var_name: str = "ANTHROPIC_API_KEY"
    client: Anthropic

    @override
    def _build_client(self, api_key: str | None):
        api_key = self._validate_api_key(api_key)
        return Anthropic(api_key=api_key)

    @override
    def _get_response_from_client(self, code: str) -> str:
        response = self.client.messages.create(
            max_tokens=MAX_TOKENS,
            model=self.model,
            messages=[
                {
                    "role": "assistant",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": code
                }
            ]
        )
        return getattr(response.content, "text", "no text input")
