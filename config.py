# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>
"""
Contains common configuration options and defaults found throughout 
the codebase.
"""

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

DEFAULT_MODEL = "gpt-5-nano"

MAX_TOKENS = 1024
