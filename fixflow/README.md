# FixFlow — Context-Aware AI Bug Fixer (final)

Flask app that turns broken Python plus an error into a separate explanation and proposed fix using two Chat Completions calls, keeps multi-turn chat context, and uses deliberate model/parameter defaults.

## Setup

1. Create and activate a virtual environment (Python 3.7+).
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`, or export the variable in your shell.
4. From this folder, run the scripted verify:

```bash
python verify_e2e.py
```

5. Start the app:

```bash
export FLASK_APP=app.py
flask run
```

Or: `python app.py`

6. Open the printed local URL. Click **Fix Code** on the prefilled empty-list `average([])` crash, then send the follow-up `make the guard return None` in chat.

## Documented defaults (`app.py`)

- `FIXFLOW_MODEL = "gpt-4o-mini"` — light chat model for clear traceback cases
- `FIXFLOW_TEMPERATURE = 0.2` — focused, low-randomness completions
- `FIXFLOW_MAX_TOKENS = 500` — room for a short explanation or a full fixed function

## Acceptance checks (sample failure)

1. API key is loaded from the environment only
2. Explanation blames empty-length division by zero
3. Proposed fix is a complete guarded function
4. `finish_reason` is `stop` on both explain and fix completions
5. Follow-up chat still refers to the average empty-list bug

Optional model bake-off: `python compare_models.py`

## Routes

- `GET /` — chat + bug-fix UI
- `POST /fix` — two completions (`explanation`, `fixed_code`)
- `POST /chat` — multi-turn chat against `conversation_history`

## Note

`conversation_history` is in-process memory. Restarting the server clears it.
