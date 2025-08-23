# AGENTS Instructions

Applies to all files in `tests/`.

## Guidelines
- Use `pytest` with test functions named `test_*`.
- Keep tests isolated and deterministic; mock external resources such as network or filesystem.
- Structure tests to mirror the backend modules they cover.

## Running
- Execute `pytest` from the repository root after modifying tests or source code.

## Status

### Implemented
- Single unit test verifying calorie calculations.

### Missing
- Tests for API routers, database operations, and LLM connectors.
- Any frontend-related tests.
