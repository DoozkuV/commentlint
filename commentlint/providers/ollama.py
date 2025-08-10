# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>
from typing import override
from ollama import Client 

from .base import LLMProvider


class OllamaProvider(LLMProvider):
    provider: str = "Ollama"
    client: Client

    @override
    def _build_client(self, api_key: str | None):
        return Client()

    @override
    def _get_response_from_client(self, code: str) -> str:
        response = self.client.chat(
            model=self.model, 
            messages=[
                {
                    "role": "assistant", 
                    "content": self.prompt
                },
                {
                    'role': 'user',
                    'content': code
                }
            ]
        )

        return response.message.content or "no response"



