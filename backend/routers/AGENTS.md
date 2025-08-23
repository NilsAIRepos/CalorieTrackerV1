# AGENTS Instructions

Guidelines for REST API routers.

## Guidelines
- Each module must expose an `APIRouter` instance named `router`.
- Group related endpoints in the same file; keep unrelated resources separate.
- Route handlers should be async and validate input with Pydantic models.
- Include concise docstrings describing each endpoint's purpose.

## Testing
- Use FastAPI's `TestClient` to cover success and failure cases.
- Avoid relying on external services in router tests; mock when necessary.

## Status

### Implemented
- `entries` router for storing and listing meals.
- `llm` router to proxy chat messages to selected providers.

### Missing
- Routers for image upload, barcode lookup, food database search, and voice transcription.
- Validation and error handling around LLM-driven conversations.
