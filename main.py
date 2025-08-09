#!/usr/bin/env python3
import sys
import os 
import json 
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

Source code: 
{code}
"""

# This code checks where the file is and does nothing
def check_file(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    prompt = PROMPT_TEMPLATE.format(code=code)

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        issues = json.loads(raw_output)
    except json.JSONDecodeError:
        print(f"{path}:0: error: LLM returned invalid JSON")
        return

    for issue in issues:
        line = issue.get("line", 0)
        comment = issue.get("comment", "").replace("\n", " ")
        reason = issue.get("issue", "").replace("\n", " ")
        print(f"{path}:{line}: error: {reason} | Comment: {comment}")

def main():
    if len(sys.argv) < 2:
        print("Usage: commentlint.py <file1> [file2 ...]")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        if os.path.isfile(file_path):
            check_file(file_path)
        else:
            print(f"{file_path}:0: error: File not found")


# This is a no-op
if __name__ == "__main__":
    main()
