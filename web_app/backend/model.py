import os
import numpy as np
from PIL import Image
import logging

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("TensorFlow not installed. Models will not load. Using mock fallback.")

from config import BINARY_MODEL_PATH, MULTI_MODEL_PATH, INFERENCE_TARGET_SIZE, INFERENCE_CONFIDENCE_THRESHOLD

# Configure logging
logger = logging.getLogger(__name__)

binary_model_path = str(BINARY_MODEL_PATH)
multi_model_path = str(MULTI_MODEL_PATH)

binary_model = None
multi_model = None

def load_models():
    global binary_model, multi_model
    if not TF_AVAILABLE:
        logger.warning("TensorFlow not available - using mock fallback")
        return
    try:
        if os.path.exists(binary_model_path):
            logger.info(f"Loading binary model from {binary_model_path}")
            binary_model = tf.keras.models.load_model(binary_model_path, compile=False)
        else:
            logger.warning(f"Binary model not found at {binary_model_path}")
            
        if os.path.exists(multi_model_path):
            logger.info(f"Loading multi-class model from {multi_model_path}")
            multi_model = tf.keras.models.load_model(multi_model_path, compile=False)
        else:
            logger.warning(f"Multi-class model not found at {multi_model_path}")
    except Exception as e:
        logger.error(f"Error loading models: {e}", exc_info=True)

def preprocess_image(image: Image.Image, target_size=None):
    if target_size is None:
        target_size = (INFERENCE_TARGET_SIZE, INFERENCE_TARGET_SIZE)
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)

def predict(image: Image.Image, model_type: str):
    if binary_model is None and multi_model is None:
        load_models()
        
    original_size = image.size
    input_tensor = preprocess_image(image)
    
    # Mock fallback if TF is not available or model not loaded
    if not TF_AVAILABLE or (model_type == 'binary' and binary_model is None) or (model_type == 'multi' and multi_model is None):
        logger.info(f"Using mock fallback for {model_type} model")
        mask = np.zeros((256, 256, 3), dtype=np.uint8)
        # Create a simple mock mask based on center circle
        y, x = np.ogrid[-128:128, -128:128]
        mock_circle = x**2 + y**2 <= 80**2
        
        if model_type == 'binary':
            mask[mock_circle] = [0, 255, 0] # Green circle
        else:
            mask[mock_circle] = [255, 0, 0] # Red circle
            # add another circle
            mock_circle2 = (x-40)**2 + (y-40)**2 <= 40**2
            mask[mock_circle2] = [0, 0, 255] # Blue circle
            
        mask_image = Image.fromarray(mask, mode='RGB')
        mask_image = mask_image.resize(original_size, Image.NEAREST)
        return mask_image
    
    if model_type == 'binary':
        prediction = binary_model.predict(input_tensor, verbose=0)[0]
        # prediction is likely (256, 256, 1) probability map
        mask = (prediction > INFERENCE_CONFIDENCE_THRESHOLD).astype(np.uint8) * 255
        
        # Colorize binary mask to make it visible (e.g. green)
        color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
        color_mask[..., 1] = np.squeeze(mask) # Green channel
        mask = color_mask

    elif model_type == 'multi':
        prediction = multi_model.predict(input_tensor, verbose=0)[0]
        mask_class = np.argmax(prediction, axis=-1).astype(np.uint8)
        
        mask = np.zeros((*mask_class.shape, 3), dtype=np.uint8)
        colors = [
            [0, 0, 0],       # 0: Background
            [255, 0, 0],     # 1: Red
            [0, 255, 0],     # 2: Green
            [0, 0, 255],     # 3: Blue
            [255, 255, 0],   # 4: Yellow
            [255, 0, 255],   # 5: Magenta
            [0, 255, 255],   # 6: Cyan
            [255, 128, 0],   # 7: Orange
            [128, 0, 255],   # 8: Purple
            [0, 255, 128],   # 9: Spring Green
        ]
        
        for c in range(10): # Max 10 classes
            color = colors[c]
            mask[mask_class == c] = color
            
    else:
        raise ValueError("Invalid model type")
        
    mask_image = Image.fromarray(mask, mode='RGB')
    mask_image = mask_image.resize(original_size, Image.NEAREST)
    return mask_image
