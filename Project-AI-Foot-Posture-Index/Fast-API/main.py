from fastapi import FastAPI
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import base64
from service import Service

app = FastAPI()

class ImageData(BaseModel):
    image: str

@app.post("/api/predict_ic")
async def upload_image(image_data: ImageData):
    image_bytes = base64.b64decode(image_data.image)
    image = Image.open(BytesIO(image_bytes))
    # image.save("image_ic.jpg")
    
    service = Service()
    result_ic = await service.predict_ic(image)
    
    return result_ic

@app.post("/api/predict_arka")
async def upload_image(image_data: ImageData):
    image_bytes = base64.b64decode(image_data.image)
    image = Image.open(BytesIO(image_bytes))
    # image.save("image_arka.jpg")
    
    service = Service()
    result_arka = await service.predict_arka(image)
    
    return result_arka
