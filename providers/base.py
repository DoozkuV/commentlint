from abc import ABC, abstractmethod
from typing import TypedDict

PROMPT_TEMPLATE = """
You are a code-comment consistency checker.
Given the following source code, focus ONLY on the comments and documentation.
For each comment/docstring, check if it accurately describes the code it refers to.
If not, output a mismatch report in JSON array format, where each item is:
{{
  "line": <line number of the comment>,
  "comment": "<comment text>",
  "issue": "<reason it's inaccurate>"
}}

Only output valid JSON. Do not include any extra text.
"""

class Issue(TypedDict):
    line: int 
    comment: str
    issue: str

class MissingAPIKeyError(RuntimeError):
    pass

class LLMProvider(ABC): 
    """An interface for LLMProviders"""
    model: str

    def __init__(self, model: str, api_key: str | None = None) -> None:
        self.model = model

    @abstractmethod
    def get_responses_for_file(self, path: str) -> list[Issue]: pass
