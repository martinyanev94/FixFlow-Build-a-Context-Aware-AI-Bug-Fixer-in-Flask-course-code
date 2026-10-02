"""Scripted end-to-end verify for FixFlow on one sample failure."""

from __future__ import annotations

from app import (
    FIXFLOW_MAX_TOKENS,
    FIXFLOW_MODEL,
    FIXFLOW_TEMPERATURE,
    conversation_history,
    create_completion,
    explain_messages,
    fix_messages,
)

CODE = """def average(nums):
    return sum(nums) / len(nums)

print(average([]))"""

ERROR = "ZeroDivisionError: division by zero"
FOLLOW_UP = "make the guard return None"


def main() -> None:
    print("defaults:")
    print(f"  model={FIXFLOW_MODEL}")
    print(f"  temperature={FIXFLOW_TEMPERATURE}")
    print(f"  max_tokens={FIXFLOW_MAX_TOKENS}")
    print()

    explain_resp = create_completion(explain_messages(CODE, ERROR))
    explanation = explain_resp.choices[0].message.content or ""
    explain_finish = explain_resp.choices[0].finish_reason

    fix_resp = create_completion(fix_messages(CODE, ERROR))
    fixed_code = fix_resp.choices[0].message.content or ""
    fix_finish = fix_resp.choices[0].finish_reason

    print("=== explanation ===")
    print(explanation)
    print(f"finish_reason={explain_finish}")
    print()
    print("=== fixed_code ===")
    print(fixed_code)
    print(f"finish_reason={fix_finish}")
    print()

    conversation_history.append(
        {
            "role": "user",
            "content": f"Bug report:\n{CODE}\n\nError:\n{ERROR}",
        }
    )
    conversation_history.append(
        {
            "role": "assistant",
            "content": (
                f"Explanation:\n{explanation}\n\n"
                f"Proposed fix:\n{fixed_code}"
            ),
        }
    )
    conversation_history.append({"role": "user", "content": FOLLOW_UP})
    follow_resp = create_completion(conversation_history)
    follow_text = follow_resp.choices[0].message.content or ""
    follow_finish = follow_resp.choices[0].finish_reason

    print("=== follow-up ===")
    print(follow_text)
    print(f"finish_reason={follow_finish}")
    print()

    checks = {
        "explanation_nonempty": bool(explanation.strip()),
        "fixed_code_nonempty": bool(fixed_code.strip()),
        "explain_finish_stop": explain_finish == "stop",
        "fix_finish_stop": fix_finish == "stop",
        "follow_up_nonempty": bool(follow_text.strip()),
    }
    for name, ok in checks.items():
        print(f"check {name}: {'PASS' if ok else 'FAIL'}")

    if not all(checks.values()):
        raise SystemExit("End-to-end verify failed one or more checks.")
    print("End-to-end verify passed structural checks.")


if __name__ == "__main__":
    main()
