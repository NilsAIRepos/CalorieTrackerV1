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

## Getting started
1. Ensure Python and Node.js are installed.
2. Clone the repository and create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install fastapi uvicorn pytest requests
   npm install
   ```
3. Start the API and static server as shown in [Running](#running) and open the
   app in a browser.

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
- `requests` Python package for the Ollama connector

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pytest requests
npm install
```

### Running
```bash
uvicorn backend.main:app --reload  # API
python -m http.server --directory frontend 8000  # serve PWA
```

### Testing
```bash
pytest
```

## Detailed quickstart on Windows with Ollama
Follow these steps to run the app with a local LLM using only the Windows command prompt.

1. **Verify prerequisite tools**
   ```cmd
   git --version
   python --version
   node --version
   npm --version
   conda --version
   ```
   If any command fails, install the missing tool:
   - [Git for Windows](https://git-scm.com/download/win)
   - [Python](https://www.python.org/downloads/windows/) (enable "Add to PATH" during setup)
   - [Node.js](https://nodejs.org/en/download/prebuilt-installer)
   - [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

2. **Install and launch Ollama**
   - Download [Ollama for Windows](https://ollama.com/download/windows).
   - In `cmd`, confirm it works and pull a model:
     ```cmd
     ollama --version
     ollama pull llama3.2:latest
     ollama serve
     ```

3. **Clone the repository**
   ```cmd
   git clone https://github.com/your-username/CalorieTrackerV1.git
   cd CalorieTrackerV1
   ```

4. **Create and activate a Conda environment**
   ```cmd
   conda create -n calorie-tracker python=3.11 -y
   conda activate calorie-tracker
   conda info --envs
   python --version
   ```
   `conda info --envs` should show a `*` next to `calorie-tracker`, and `python --version` should display `3.11.x`.

5. **Install project dependencies**
   ```cmd
   pip install fastapi uvicorn pytest requests
   npm install
   ```

6. **Start the backend API**
   ```cmd
   uvicorn backend.main:app --reload
   ```
   Leave this window running.

7. **Start the frontend in a second `cmd` window**
   ```cmd
   conda activate calorie-tracker
   python -m http.server --directory frontend 8000
   ```

8. **Configure the LLM connector**
   - Open a browser to `http://localhost:8000`.
   - Navigate to **Settings** and enter:
     - Provider: `ollama`
     - Base URL: `http://localhost:11434`
     - Model: `llama3.2:latest`
   - Save the settings.

9. **Begin testing**
   - Add a meal entry and confirm the calorie log updates.

## Deployment
- Build the frontend with `npm run build` and serve the static assets.
- Run the FastAPI application behind a TLS termination proxy.
- Configure environment variables to select the desired LLM provider.

## Contributing
1. Fork the repository and create a feature branch.
2. Commit changes with descriptive messages.
3. Run `pytest` and ensure all checks pass.
4. Submit a pull request for review.

