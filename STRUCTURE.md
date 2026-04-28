# Project Structure Documentation

This document describes the improved project structure for PaxeraHealth AI Segmentation.

## Root Level Files

```
PaxeraHealth-AI/
├── .env                    # Development environment configuration (local)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
├── README.md               # Main project documentation
├── INSTALLATION.md         # Installation and setup guide (NEW)
├── STRUCTURE.md            # This file - structure documentation (NEW)
└── pyproject.toml          # Project metadata and dependencies (NEW)
```

## Backend Structure

```
web_app/backend/
├── __init__.py             # Package initialization (NEW)
├── .venv/                  # Virtual environment (do not commit)
├── __pycache__/            # Python cache (do not commit)
├── app.py                  # FastAPI application (UPDATED)
├── model.py                # ML model inference logic (UPDATED)
├── config.py               # Configuration management (NEW)
├── requirements.txt        # Python dependencies (NEW)
```

### File Descriptions

#### `config.py` (NEW)
Centralized configuration management. Reads from environment variables with sensible defaults.
```python
from config import BACKEND_HOST, BACKEND_PORT, MODELS_DIR
```

#### `requirements.txt` (NEW)
Python package dependencies for the backend.
- fastapi: Web framework
- uvicorn: ASGI server
- tensorflow: Deep learning framework
- pillow: Image processing
- numpy: Numerical computations

#### `app.py` (UPDATED)
- Added proper logging with configuration
- Added startup event to load models on application start
- Added health check endpoint (`/health`)
- Improved error handling and validation
- Uses config module for settings
- Better CORS configuration
- Enhanced API documentation

#### `model.py` (UPDATED)
- Uses config module for model paths and inference settings
- Proper logging with info/warning/error levels
- Uses configurable confidence threshold
- Better error handling

## Frontend Structure

```
web_app/frontend/
├── __init__.py             # Package placeholder (NEW)
├── index.html              # Main HTML file
├── script.js               # JavaScript logic
├── styles.css              # Custom CSS styles
└── test_image.png          # Test image for UI
```

## Data Structure (Improved)

```
data/
├── .gitkeep                # Keeps folder in git (NEW)
├── raw/
│   └── .gitkeep           # Keeps folder in git (NEW)
└── test/
    └── .gitkeep           # Keeps folder in git (NEW)
```

`.gitkeep` files ensure empty directories are tracked by Git.

## Models Structure

```
models/
├── best_unet_binary_scratch.keras
└── best_unet_multi_scratch.keras
```

Model files are typically ignored by Git but tracked by Git LFS if configured.

## Documentation Structure

```
root/
├── README.md               # Main project overview
├── INSTALLATION.md         # Setup and installation instructions (NEW)
└── STRUCTURE.md            # This file - architectural documentation (NEW)
```

## Configuration Management

### `.env` File Hierarchy
1. `.env` (local, do not commit) - Personal development settings
2. `.env.example` (committed) - Template with defaults

### Configuration Options

See `.env.example` for all available configuration options:
- `BACKEND_HOST`: Server address (default: 127.0.0.1)
- `BACKEND_PORT`: Server port (default: 8000)
- `BACKEND_RELOAD`: Auto-reload on code changes (default: true)
- `INFERENCE_TARGET_SIZE`: Model input size (default: 256)
- `INFERENCE_CONFIDENCE_THRESHOLD`: Binary threshold (default: 0.5)
- `LOG_LEVEL`: Logging verbosity (default: INFO)

## Key Improvements

### 1. **Dependency Management**
- ✅ `requirements.txt` for pip/uv installation
- ✅ `pyproject.toml` for modern Python packaging

### 2. **Configuration Management**
- ✅ `config.py` module centralizes settings
- ✅ `.env` template for environment variables
- ✅ Removed hardcoded values

### 3. **Code Organization**
- ✅ `__init__.py` files make directories proper Python packages
- ✅ Proper logging setup throughout
- ✅ Better error handling and validation

### 4. **Development Setup**
- ✅ `INSTALLATION.md` with step-by-step setup
- ✅ `.gitkeep` files preserve directory structure
- ✅ Virtual environment support

### 5. **Documentation**
- ✅ Project structure documentation (this file)
- ✅ API documentation in code (docstrings)
- ✅ Configuration documentation

## Directory Permissions

Ensure proper permissions for:
- `models/` - Read-only for production
- `data/` - Write access for training/inference
- `web_app/backend/` - Python code directory
- `web_app/frontend/` - Static assets

## Git Workflow

```bash
# Files to commit
.env.example              # Template (commit)
config.py                 # Code (commit)
requirements.txt          # Dependencies (commit)
pyproject.toml            # Metadata (commit)
INSTALLATION.md           # Documentation (commit)

# Files to ignore (in .gitignore)
.env                      # Local configuration
.venv/                    # Virtual environment
__pycache__/              # Python cache
*.pyc                     # Compiled Python
models/                   # Large model files (optional)
```

## Deployment Considerations

### Production Checklist
- [ ] `.env.example` has all required variables
- [ ] `.env` contains production values
- [ ] `LOG_LEVEL=ERROR` in production
- [ ] `BACKEND_RELOAD=false` in production
- [ ] Models are properly mounted/downloaded
- [ ] CORS is configured for your domain
- [ ] Health check endpoint works
- [ ] Error handling is comprehensive

### Docker Support (Future)
Structure is ready for Dockerfile:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY web_app/backend /app
CMD ["python", "app.py"]
```

## Related Documentation

- 📖 [Main README](README.md) - Project overview
- 🚀 [Installation Guide](INSTALLATION.md) - Setup instructions
- ⚙️ [Backend Config](web_app/backend/config.py) - Configuration code
- 🏗️ [FastAPI Docs](http://localhost:8000/docs) - API documentation (when running)
