# Installation and Setup Guide

This document provides step-by-step instructions for setting up the PaxeraHealth AI Segmentation project.

## Prerequisites

- **Python 3.10+** (Download from [python.org](https://www.python.org/downloads/))
- **pip** or **uv** (Python package manager)

## Installation Steps

### Option 1: Using Python's `venv` (Recommended)

#### 1. Clone or Navigate to the Project
```bash
cd path/to/PaxeraHealth-AI
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv web_app\backend\.venv

# On macOS/Linux
python3 -m venv web_app/backend/.venv
```

#### 3. Activate Virtual Environment
```bash
# On Windows
web_app\backend\.venv\Scripts\activate

# On macOS/Linux
source web_app/backend/.venv/bin/activate
```

#### 4. Upgrade pip
```bash
pip install --upgrade pip
```

#### 5. Install Dependencies
```bash
pip install -r web_app/backend/requirements.txt
```

### Option 2: Using `uv` (Fast Alternative)

```bash
cd web_app/backend
uv sync
```

## Environment Configuration

#### 1. Copy Environment Template
```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

#### 2. Edit `.env` File (Optional)
Customize configuration values as needed (default values work for local development):
```
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
BACKEND_RELOAD=true
```

## Starting the Application

### Option 1: Windows Batch Script (Easiest)
```bash
# Double-click the file or run from command prompt:
web_app\run_app.bat
```

### Option 2: Manual Backend Start
```bash
cd web_app/backend
python app.py
# or
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at `http://127.0.0.1:8000`

### Option 3: Frontend in Separate Terminal
```bash
# Terminal 1 - Backend
cd web_app/backend
python app:app --reload

# Terminal 2 - Frontend (optional, for development)
# Navigate to web_app/frontend in a browser:
# http://127.0.0.1:8000
```

## Verifying Installation

### Check Backend Health
```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{"status": "healthy", "service": "PaxeraHealth Segmentation API"}
```

### Access the Web App
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## Project Structure

```
.
├── web_app/
│   ├── backend/               # FastAPI backend
│   │   ├── app.py            # Main application
│   │   ├── model.py          # ML model inference
│   │   ├── config.py         # Configuration management
│   │   └── requirements.txt   # Python dependencies
│   └── frontend/              # Vanilla JS frontend
│       ├── index.html
│       ├── script.js
│       └── styles.css
├── models/                     # Saved model weights
├── data/                       # Training and test data
├── notebooks/                  # Jupyter notebooks
├── pyproject.toml             # Project metadata
├── .env.example               # Environment template
└── .gitignore                 # Git ignore rules
```

## Troubleshooting

### Models Not Found
Ensure the `.keras` files exist in the `models/` directory:
- `models/best_unet_binary_scratch.keras`
- `models/best_unet_multi_scratch.keras`

### Port Already in Use
If port 8000 is already in use, modify `.env`:
```
BACKEND_PORT=8001
```

### TensorFlow Installation Issues
On Windows, you may need Visual C++ build tools. For GPU support:
```bash
pip install tensorflow[and-cuda]
```

### Module Not Found Errors
Ensure your virtual environment is activated:
```bash
# On Windows - should show (.venv) in terminal
web_app\backend\.venv\Scripts\activate

# On macOS/Linux - should show (.venv) in terminal
source web_app/backend/.venv/bin/activate
```

## Development

### Running Tests
```bash
pip install pytest pytest-asyncio
pytest
```

### Code Formatting
```bash
pip install black
black web_app/backend/
```

### Linting
```bash
pip install flake8
flake8 web_app/backend/
```

## Support

For issues or questions, please open an issue on GitHub or contact the development team.
