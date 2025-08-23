# AGENTS Instructions

Rules for the pluggable LLM connectors.

## Guidelines
- Each provider module must subclass `LLMBase` from `base.py` and implement its abstract methods.
- Provider configuration should come from environment variables accessed via `os.getenv`.
- Avoid heavy dependencies; keep connectors self-contained and optional.
- Expose an async `generate(prompt: str) -> str` method returning only the model text.

## Testing
- Network calls must be mocked in unit tests.
- Add tests for any new connector logic under `tests/`.

## Status

### Implemented
- Base abstraction plus connectors for a dummy local model, Ollama REST API, and OpenAI chat API.

### Missing
- Connectors for additional providers such as Anthropic or llama.cpp.
- Streaming responses and advanced error handling.
- Unit tests covering existing connectors.
