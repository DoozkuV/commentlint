#!/usr/bin/env python3
import sys
import os 
from providers.base import Issue
from providers.models import create_model

MODEL_NAME = "gpt-5"

# This code checks where the file is and does nothing
def print_issues_for_path(issues: list[Issue], path: str) -> None:
    for issue in issues:
        line = issue.get("line", 0)
        comment = issue.get("comment", "").replace("\n", " ")
        reason = issue.get("issue", "").replace("\n", " ")
        print(f"{path}:{line}: error: {reason} | Comment: {comment}")

def main():
    """Main logic of the program"""
    if len(sys.argv) < 2:
        print("Usage: commentlint.py <file1> [file2 ...]")
        sys.exit(1)

    model = create_model(MODEL_NAME)
    for file_path in sys.argv[1:]:
        if os.path.isfile(file_path):
            issues = model.get_responses_for_file(file_path)
            print_issues_for_path(issues, file_path)
        else:
            print(f"{file_path}:0: error: File not found")


# This is a no-op
if __name__ == "__main__":
    main()
