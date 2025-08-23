# AGENTS Instructions

This file covers all Python modules under the backend directory.

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

## Status

### Implemented
- `calorie_engine.py` for nutrient-based calculations and `db.py` for SQLite persistence.
- Routers for meal entry CRUD and basic LLM chat proxying.
- Connectors for local dummy, Ollama, and OpenAI models.

### Missing
- Processors and endpoints for images, barcodes, voice input, and database search.
- Orchestrator tying LLM responses to entry creation.
- Comprehensive unit tests for routers and connectors.
