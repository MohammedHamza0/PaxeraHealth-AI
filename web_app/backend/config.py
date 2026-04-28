"""
Configuration module for the PaxeraHealth Segmentation Backend.
Reads from environment variables with sensible defaults.
"""

import os
from pathlib import Path

# Get the base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Backend Server Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
BACKEND_RELOAD = os.getenv("BACKEND_RELOAD", "false").lower() == "true"

# Frontend Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:8000")

# Model Configuration
MODELS_DIR = BASE_DIR / Path(os.getenv("MODEL_DIR", "models"))
BINARY_MODEL_PATH = MODELS_DIR / os.getenv("BINARY_MODEL_PATH", "best_unet_binary_scratch.keras")
MULTI_MODEL_PATH = MODELS_DIR / os.getenv("MULTI_MODEL_PATH", "best_unet_multi_scratch.keras")

# Inference Configuration
INFERENCE_TARGET_SIZE = int(os.getenv("INFERENCE_TARGET_SIZE", 256))
INFERENCE_CONFIDENCE_THRESHOLD = float(os.getenv("INFERENCE_CONFIDENCE_THRESHOLD", 0.5))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Display configuration on startup
def print_config():
    """Print the active configuration (useful for debugging)."""
    print("=" * 60)
    print("PaxeraHealth Backend Configuration")
    print("=" * 60)
    print(f"Host: {BACKEND_HOST}")
    print(f"Port: {BACKEND_PORT}")
    print(f"Reload: {BACKEND_RELOAD}")
    print(f"Models Directory: {MODELS_DIR}")
    print(f"Binary Model: {BINARY_MODEL_PATH.name}")
    print(f"Multi Model: {MULTI_MODEL_PATH.name}")
    print("=" * 60)
