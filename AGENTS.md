# AGENTS Instructions

Welcome to the Calorie Tracker project. The following guidelines keep contributions consistent and easy to maintain.

## Background & Vision
- Lightweight calorie tracker that logs daily intake with a beautiful, modern UI.
- Users can record meals by snapping a picture, scanning a barcode, typing or searching text, querying a product database, or speaking answers aloud.
- An LLM acts as a conversational assistant to gather missing context, but the final calorie numbers are computed by deterministic Python code.
- The app is a Progressive Web App that runs on mobile and desktop, works offline, and stores databases and personal data client-side for privacy.
- LLM connectors are pluggable so contributors can switch between local models (e.g., llama.cpp, Ollama) and remote providers (OpenAI, Anthropic, etc.).

## Design Philosophy
- **User-first UX:** keep flows intuitive, reduce friction, and ensure responsive, accessible layouts.
- **Privacy & Ownership:** all persistent data lives on the user's device; avoid server-side state except for request processing.
- **Modularity:** implement features as small, testable units; new input methods or LLM providers should extend existing interfaces.
- **Determinism:** calorie calculations use classical formulas; the LLM only helps collect structured information.
- **Progressive Enhancement:** the PWA should remain functional with limited connectivity or browser capabilities.

## Repository Layout
- **backend/** – FastAPI application and business logic
  - `calorie_engine.py` – deterministic calorie computations
  - `db.py` – SQLite persistence
  - `llm/` – pluggable connectors (OpenAI, Ollama, local, etc.)
  - `routers/` – REST endpoints (meal entries, LLM interaction)
- **frontend/** – vanilla JS Progressive Web App with offline capability
  - `index.html`, `app.js`, `style.css` – main UI
  - `settings.html`/`settings.js` – LLM configuration page
  - `service-worker.js`, `manifest.json` – PWA assets
- **tests/** – pytest test suite

## Development
- Target Python 3.10+ and keep code modular with type hints.
- Follow the interface in `backend/llm/base.py` when adding new LLM providers.
- Keep the frontend framework-free; prefer small, accessible components.
- User data and databases are client-side; backend should remain stateless beyond request handling.

## Style
- **Python:** PEP 8, four-space indentation, include docstrings for public functions.
- **JavaScript:** modern ES6+, two-space indentation, semicolons required.
- **HTML/CSS:** keep markup minimal and responsive.

## Testing
- Run `pytest` from the repo root after every change.
- Ensure the working tree is clean and all tests pass before committing.

## Tooling
- Prefer `rg` for searching the codebase; avoid expensive recursive commands.
- Commit messages should be short and in the imperative mood (e.g., "Add OAuth connector").

