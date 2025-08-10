import json
import os
from typing import cast, override
from anthropic import Anthropic
from .base import Issue, LLMProvider, PROMPT_TEMPLATE, MissingAPIKeyError

MAX_TOKENS = 1024

class AnthropicAIProvider(LLMProvider):
    client: Anthropic

    def __init__(self, model: str, api_key: str | None = None):
        super().__init__(model)
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise MissingAPIKeyError(
                "Anthropic API key is not set. " + 
                "Pass it explicitly or set the OPENAI_API_KEY environment variable."
            )
        self.client = Anthropic(api_key=api_key)

    @override
    def get_responses_for_file(self, path: str) -> list[Issue]:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        response = self.client.messages.create(
            max_tokens=MAX_TOKENS,
            model=self.model,
            messages=[
                {
                    "role": "assistant",
                    "content": PROMPT_TEMPLATE
                },
                {
                    "role": "user",
                    "content": code
                }
            ]
        )

        response_text = getattr(response.content, "text", "no text input")
        try:
            return cast(list[Issue], json.loads(response_text))
        except json.JSONDecodeError:
            return [{
                "line": 0,
                "issue": "LLM returned invalid JSON",
                "comment": response_text
            }]
