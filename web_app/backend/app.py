import logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
import io
import os
from pathlib import Path
from PIL import Image
from model import predict, load_models
from config import BACKEND_HOST, BACKEND_PORT, BACKEND_RELOAD, LOG_LEVEL, FRONTEND_URL, print_config

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PaxeraHealth Segmentation Web App",
    description="AI-powered medical image segmentation API",
    version="1.0.0"
)

# Print configuration on startup
logger.info("Starting PaxeraHealth Segmentation Backend")
print_config()

# Load models on startup
@app.on_event("startup")
async def startup_event():
    """Load ML models on application startup."""
    logger.info("Loading ML models...")
    load_models()
    logger.info("Models loaded successfully")

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict", tags=["Predictions"])
async def run_prediction(file: UploadFile = File(...), model_type: str = Form(...)):
    """
    Run segmentation prediction on an uploaded image.
    
    Args:
        file: Image file to segment (JPG, PNG, etc.)
        model_type: Type of segmentation ('binary' or 'multi')
    
    Returns:
        PNG image with segmentation mask overlay
    """
    try:
        if model_type not in ['binary', 'multi']:
            raise HTTPException(status_code=400, detail="model_type must be 'binary' or 'multi'")
        
        logger.info(f"Processing prediction request for {model_type} segmentation")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        logger.debug(f"Image loaded: {image.size}")
        
        # Predict
        mask_image = predict(image, model_type)
        
        # Convert mask to bytes
        img_byte_arr = io.BytesIO()
        mask_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img_byte_arr = img_byte_arr.getvalue()
        
        logger.info(f"Prediction completed successfully for {model_type} model")
        
        return Response(content=img_byte_arr, media_type="image/png")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "PaxeraHealth Segmentation API"}

# Mount frontend files - must be done AFTER all API routes
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    logger.info(f"Mounting frontend from: {frontend_path}")
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    logger.warning(f"Frontend directory not found at: {frontend_path}")

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {BACKEND_HOST}:{BACKEND_PORT}")
    uvicorn.run(
        "app:app",
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        reload=BACKEND_RELOAD
    )
