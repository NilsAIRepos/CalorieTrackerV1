# Calorie Tracker V1

## Overview
Calorie Tracker V1 is a local-first calorie logging application that helps users
estimate their daily intake with the assistance of large language models (LLMs).
The app is designed as a Progressive Web Application (PWA) that runs on mobile
and desktop browsers and stores all data on the user's device.

## Features
- **Multiple input methods**: log meals by taking a photo, scanning a barcode,
  searching a food database, typing free text, or speaking with voice input.
- **LLM-guided dialogue**: an LLM asks follow-up questions to gather missing
  information and interpret the user's responses.
- **Local data storage**: the food database, user profile, and daily logs reside
  entirely on the user's machine.
- **Flexible model providers**: easily switch between local models (e.g.
  `llama.cpp`, `ollama`) and remote APIs such as OpenAI or Anthropic.
- **Deterministic calorie engine**: calories are calculated with traditional
  Python code; the LLM only supplies the required parameters.


## Architecture
Calorie Tracker V1 uses a modular Python backend with a PWA frontend.

### Component overview
1. **User Interface (PWA)**
   - Built with modern web technologies and packaged with a service worker for
     offline use.
   - Communicates with the backend over HTTPS/JSON.
2. **API & Logic Layer (Python/FastAPI)**
   - REST endpoints for logging entries, image upload, barcode lookup, and food
     search.
   - Input processors handle photos, barcodes, text queries, and voice clips.
   - A conversation orchestrator interacts with pluggable LLM providers to
     collect missing details.
   - The calorie engine computes nutritional values using validated formulas.
3. **Storage**
   - Client-side SQLite database accessed via WebAssembly or browser storage.
   - Optional export/import for backups.
4. **LLM Connectors**
   - Provider-agnostic interface selecting an implementation at runtime.
   - Supports local models and remote APIs through environment configuration.

### Data flow
1. User submits information through one of the input methods.
2. Backend processors normalize the data and invoke the LLM orchestrator when
   additional context is needed.
3. The LLM returns structured meal attributes.
4. The calorie engine calculates total calories and returns results to the UI.
5. Entries are saved into the client-side database and visualized for the user.

### API sketch
- `POST /log` – add a meal entry.
- `POST /image` – upload a meal photo for analysis.
- `GET /barcode/{code}` – fetch product data via barcode.
- `GET /food/search?q=` – query the food database.
- `WS /voice` – stream voice input for transcription.

## Development
### Requirements
- Python 3.11+
- Node.js and a modern package manager (for PWA build tooling)


### Setup
```bash
python -m venv .venv
source .venv/bin/activate


### Running
```bash


### Testing
```bash
pytest
```

## Deployment
- Build the frontend with `npm run build` and serve the static assets.
- Run the FastAPI application behind a TLS termination proxy.
- Configure environment variables to select the desired LLM provider.

## Contributing
1. Fork the repository and create a feature branch.
2. Commit changes with descriptive messages.
3. Run `pytest` and ensure all checks pass.
4. Submit a pull request for review.

