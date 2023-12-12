from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

MODEL=tf.keras.models.load_model('../models/1')
CLASS_NAMES=["Early Blight","Late Blight","Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    image = read_file_as_image(await file.read())
    predictions=MODEL.predict(np.expand_dims(image, axis=0))  #actually we are sending a single image but our ML model is trained for a batch of Images so we use np.expand_dims to add a new dimension to the image
    
    predicted_class=np.argmax(predictions[0])
    confidence=np.max(predictions[0])
    
    return {
        'class': CLASS_NAMES[predicted_class],
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)