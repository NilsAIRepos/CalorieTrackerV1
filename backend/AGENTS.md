# AGENTS Instructions

This file covers all Python modules under the backend directory.

## Status
- `main.py` wires placeholder routers for barcode, image, search, and voice features.
- A stub Anthropic connector loads dynamically; other providers and real LLM calls are absent.
- Persistence modules (`db.py`) and the calorie engine are referenced but not yet implemented.

## Guidelines
- Use asynchronous FastAPI route handlers where possible.
- Keep business logic in small, pure functions; persist data only via `db.py`.
- Provide type hints and docstrings for all public functions and classes.
- Any new settings must be injectable via environment variables or function parameters; avoid global state.

## LLM Connectors
- New LLM providers should live in the `llm/` subpackage and implement the interface defined in `base.py`.
- Connector modules should expose a `create_client()` helper returning an object with a `generate()` coroutine.

## Testing
- Add or update unit tests under `tests/` when modifying backend code.
- Run `pytest` from the repository root after changes.
