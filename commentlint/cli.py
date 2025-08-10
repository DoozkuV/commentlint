#!/usr/bin/env python3
# License: GPLv3 Copyright: 2025, George Padron <georgenpadron@gmail.com>

import argparse
import sys
import os
from typing import cast 
from .config import DEFAULT_MODEL
from .providers.models import create_model

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CommentLint - LLM-powered code comment consistency checker"
    )
    _ = parser.add_argument(
        "files",
        nargs="+",
        help="One or more source files to check"
    )
    _ = parser.add_argument(
        "--model",
        help="Model name to use (overrides COMMENTLINT_MODEL env var)",
    )
    _ = parser.add_argument(
        "--api-key",
        help="API Key for model to use (overrides [MODEL_PROVIDER]_API_KEY env var)",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    model_name = (
        cast(str, args.model)
        or os.getenv("COMMENTLINT_MODEL")
        or DEFAULT_MODEL
    )

    try: 
        model = create_model(model_name, args.api_key)
    except ValueError as e: 
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    for file_path in cast(list[str], args.files):
        if os.path.isfile(file_path):
            issues = model.get_responses_for_file(file_path)
            for issue in issues: 
                print(issue)
        else: 
            print(f"{file_path}:0: error: File not found")


# This is a no-op
if __name__ == "__main__":
    main()
