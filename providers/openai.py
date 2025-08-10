import json
import os
from typing import cast, override
from openai import OpenAI
from .base import Issue, LLMProvider, PROMPT_TEMPLATE, MissingAPIKeyError

class OpenAIProvider(LLMProvider):
    client: OpenAI

    def __init__(self, model: str, api_key: str | None = None):
        super().__init__(model)
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise MissingAPIKeyError(
                "OpenAI API key is not set. " + 
                "Pass it explicitly or set the OPENAI_API_KEY environment variable."
            )
        self.client = OpenAI(api_key=api_key)

    @override
    def get_responses_for_file(self, path: str) -> list[Issue]:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        response = self.client.responses.create(
            model=self.model,
            instructions=PROMPT_TEMPLATE,
            input=code,
        )

        try:
            return cast(list[Issue], json.loads(response.output_text))
        except json.JSONDecodeError:
            return [{
                "line": 0,
                "issue": "LLM returned invalid JSON",
                "comment": response.output_text
            }]
