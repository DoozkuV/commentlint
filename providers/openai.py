# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>
from typing import override
from openai import OpenAI
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    provider: str = "OpenAI"
    env_var_name: str = "OPENAI_API_KEY"
    client: OpenAI

    @override
    def _build_client(self, api_key: str | None):
        api_key = self._validate_api_key(api_key)
        return OpenAI(api_key=api_key)

    @override
    def _get_response_from_client(self, code: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=self.prompt,
            input=code,
        )
        return response.output_text
