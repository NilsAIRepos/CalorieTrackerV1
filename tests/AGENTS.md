# AGENTS Instructions

Applies to all files in `tests/`.

## Status
- Basic tests cover placeholder routers and the Anthropic connector stub.
- Upcoming business logic, database access, and frontend modules lack coverage.

## Guidelines
- Use `pytest` with test functions named `test_*`.
- Keep tests isolated and deterministic; mock external resources such as network or filesystem.
- Structure tests to mirror the backend modules they cover.

## Running
- Execute `pytest` from the repository root after modifying tests or source code.
