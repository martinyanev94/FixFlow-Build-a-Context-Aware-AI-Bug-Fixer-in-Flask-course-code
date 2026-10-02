# Course projects

Build FixFlow—a Flask AI bug fixer with Chat Completions—in about 48 minutes: a web app that keeps multi-turn chat context and turns a broken snippet into an explanation plus a proposed fix. You start with the project payoff and a secured first API call, then ship one core skill per lesson until the full explain-and-fix flow works end to end. You w

This repository contains the runnable project code built throughout the course.
Each lesson evolves these files; the repository stores the final working state
instead of disconnected per-lesson snippets.

## Projects and run commands

### `fixflow`

```bash
cd fixflow
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Suggested workflow

1. Clone the repository.
2. Enter the project directory shown above.
3. Install dependencies with the listed command.
4. Run the app or script, then run its tests where provided.
5. Complete the final project in `FINAL_PROJECT.md`.
