"""Compare two chat models on the same FixFlow bug prompt."""

from __future__ import annotations

import os

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Set OPENAI_API_KEY in your environment before running.")

client = OpenAI(api_key=api_key)

PROMPT = {
    "role": "user",
    "content": (
        "Explain why this crashes, then propose a fix.\n\n"
        "def average(nums):\n"
        "    return sum(nums) / len(nums)\n\n"
        "print(average([]))"
    ),
}

MODELS = ("gpt-4o-mini", "gpt-4o")


def main() -> None:
    for model_name in MODELS:
        response = client.chat.completions.create(
            model=model_name,
            messages=[PROMPT],
            temperature=0.2,
            max_tokens=500,
        )
        print("=" * 60)
        print(f"model={model_name}")
        print(response.choices[0].message.content)
        print()


if __name__ == "__main__":
    main()
