# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import os
from typing import Any, cast, override
from config import PROMPT_TEMPLATE 

@dataclass
class Issue:
    """A class representing a comment issue"""
    path: str
    line: int 
    comment: str
    issue: str

    @override
    def __str__(self) -> str:
        return f"{self.path}:{self.line}: error: {self.issue} | Comment: {self.comment}"

class LLMProvider(ABC): 
    """An interface for LLM Providers"""
    model: str
    client: Any
    prompt: str = PROMPT_TEMPLATE
    provider: str 
    env_var_name: str

    def __init__(self, model: str, api_key: str | None = None) -> None:
        self.model = model
        self.client = self._build_client(api_key)

    @abstractmethod
    def _build_client(self, api_key: str | None) -> Any:
        """Create and return the API client for this provider."""
        pass

    @abstractmethod
    def _get_response_from_client(self, code: str) -> str:
        """Send the request to the LLM and return the raw text output."""
        pass

    def _validate_api_key(self, api_key: str | None) -> str: 
        """Ensures there is a valid api_key, otherwise raises MissingAPIKeyError"""
        api_key = api_key or os.getenv(self.env_var_name)
        if not api_key:
            raise MissingAPIKeyError(
                f"{self.provider} API key is not set. " +
                f"Pass it explicitly or set {self.env_var_name}."
            )
        return api_key

    def get_responses_for_file(self, path: str) -> list[Issue]: 
        """Common logic for reading file, sending to LLM, and parsing JSON"""
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        try:
            response_text = self._get_response_from_client(code)
        except Exception as e:
            return [
                Issue(
                    path=path,
                    line=0,
                    issue="Error communicating with LLM",
                    comment=str(e),
                )
            ]
        try:
            data = cast(list[dict[str, Any]], json.loads(response_text))
            return [Issue(**fields, path=path) for fields in data]
        except json.JSONDecodeError:
            return [
                Issue(
                    path=path,
                    line=0,
                    issue="LLM returned invalid JSON",
                    comment=response_text,
                )
            ]

class MissingAPIKeyError(RuntimeError):
    pass
