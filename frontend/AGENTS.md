# AGENTS Instructions

Applies to all files in `frontend/`.

## Guidelines
- Write vanilla ES6+ JavaScript with two-space indentation and semicolons.
- Keep components small and framework-free; prefer plain HTML elements and CSS.
- Store user data in `localStorage` or IndexedDB; never call the backend for persistence.
- Ensure PWA assets (`service-worker.js`, `manifest.json`) remain valid after changes.
- Design UI with mobile-first responsiveness.

## Testing
- Frontend currently lacks automated tests; when adding any, place them under `tests/` and run `pytest` to ensure backend still passes.
