"""FixFlow lesson 1: one secured Chat Completions call."""

from __future__ import annotations

import os

from openai import OpenAI


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Set OPENAI_API_KEY in your environment before running."
        )

    client = OpenAI(api_key=api_key)

    buggy_snippet = """def average(nums):
    return sum(nums) / len(nums)

print(average([]))"""

    user_prompt = (
        "This Python crashes on empty input. "
        "Explain why, then propose a fixed function.\n\n"
        f"{buggy_snippet}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_prompt}],
    )

    assistant_text = response.choices[0].message.content
    print(assistant_text)


if __name__ == "__main__":
    main()
