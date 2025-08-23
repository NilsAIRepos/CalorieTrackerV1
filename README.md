# Calorie Tracker V1

## Overview
Calorie Tracker V1 is a local-first calorie logging application that helps users estimate their daily intake with the assistance of large language models (LLMs). The app is designed as a Progressive Web Application (PWA) that runs on mobile and desktop browsers and stores all data on the user's device.

## Features
- **Multiple input methods**: log meals by taking a photo, scanning a barcode, searching a food database, typing free text, or speaking with voice input.
- **LLM-guided dialogue**: an LLM asks follow-up questions to gather missing information and interpret the user's responses.
- **Local data storage**: the food database, user profile, and daily logs reside entirely on the user's machine.
- **Flexible model providers**: easily switch between local models (e.g., `llama.cpp`, `ollama`) and remote APIs such as OpenAI or Anthropic.
- **Deterministic calorie engine**: calories are calculated with traditional Python code; the LLM only supplies the required parameters.

## Quickstart (Windows)
The steps below walk through running the project and connecting an Ollama model on a Windows machine using Command Prompt.

### 1. Verify prerequisites
Install [Git](https://git-scm.com/), [Miniconda](https://docs.conda.io/en/latest/miniconda.html), [Python](https://www.python.org/) 3.10+, [Node.js](https://nodejs.org/) 18+, and [Ollama for Windows](https://ollama.com/). Then open **cmd** and check the versions:

```cmd
python --version
conda --version
node --version
npm --version
git --version
ollama --version
```
Each command should print a version number.

### 2. Create and activate a Conda environment

```cmd
conda create -n calorie-tracker python=3.10 -y
conda activate calorie-tracker
```

### 3. Clone the repository and install dependencies

```cmd
git clone <repo-url>
cd CalorieTrackerV1
pip install fastapi uvicorn pydantic requests
```

The frontend uses plain HTML and JavaScript, so no Node packages are required.

### 4. Prepare Ollama with the LLaMA model

```cmd
ollama pull llama3.2:latest
ollama list
```

Confirm that `llama3.2:latest` appears in the list.

### 5. Run the application

```cmd
uvicorn backend.main:app --reload
```

Open a browser to `http://localhost:8000`.

### 6. Configure the LLM connection in the UI
Click **Settings** in the top of the page and fill in:

- **Provider:** `ollama`
- **Base URL:** `http://localhost:11434`
- **Model:** `llama3.2:latest`

Click **Save** and **Test** to verify the LLM responds.

### 7. Run tests

```cmd
pytest
```

Stop the `uvicorn` server with `Ctrl+C` when finished.

## Implementation Status

### Implemented
- Manual form-based meal logging stored in a local SQLite database.
- Deterministic calorie calculations via macronutrient formula.
- Basic PWA with service worker and LLM provider settings page.
- Pluggable LLM connectors for a local dummy model, Ollama, and OpenAI.

### Missing / Planned
- Photo analysis, barcode scanning, food database search, and voice input.
- LLM-guided dialogue to collect missing meal details.
- Routers and frontend components for the advanced input methods listed above.
- Broader automated test coverage.

## Architecture
Calorie Tracker V1 uses a modular Python backend with a PWA frontend.

### Component overview
1. **User Interface (PWA)**
   - Built with modern web technologies and packaged with a service worker for offline use.
   - Communicates with the backend over HTTPS/JSON.
2. **API & Logic Layer (Python/FastAPI)**
   - REST endpoints for logging entries, image upload, barcode lookup, and food search.
   - Input processors handle photos, barcodes, text queries, and voice clips.
   - A conversation orchestrator interacts with pluggable LLM providers to collect missing details.
   - The calorie engine computes nutritional values using validated formulas.
3. **Storage**
   - Client-side SQLite database accessed via WebAssembly or browser storage.
   - Optional export/import for backups.
4. **LLM Connectors**
   - Provider-agnostic interface selecting an implementation at runtime.
   - Supports local models and remote APIs through environment configuration.

### Data flow
1. User submits information through one of the input methods.
2. Backend processors normalize the data and invoke the LLM orchestrator when additional context is needed.
3. The LLM returns structured meal attributes.
4. The calorie engine calculates total calories and returns results to the UI.
5. Entries are saved into the client-side database and visualized for the user.

### API sketch
- `POST /log` – add a meal entry.
- `POST /image` – upload a meal photo for analysis.
- `GET /barcode/{code}` – fetch product data via barcode.
- `GET /food/search?q=` – query the food database.
- `WS /voice` – stream voice input for transcription.
