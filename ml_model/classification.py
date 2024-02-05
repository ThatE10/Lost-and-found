from PIL import Image  # import pillow
import requests
from starlette.requests import Request

CONFIG_run_local = True
CONFIG_classification_API = ''
from fastapi import FastAPI

app = FastAPI()


class ml_core():

    def __init__(self, run_local=CONFIG_run_local, classification_API=CONFIG_classification_API):
        self.run_local = run_local
        if run_local:
            from io import BytesIO
            from fastapi import FastAPI, File
            from transformers import BlipProcessor, BlipForConditionalGeneration
            import torch

            self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            self.processor = BlipProcessor.from_pretrained("noamrot/FuseCap")
            self.model = BlipForConditionalGeneration.from_pretrained("noamrot/FuseCap").to(self.device)

            @app.get("/predict")
            def predict(image: bytes = File(...)):
                raw_image = Image.open(BytesIO(image))
                text = "a picture of "
                inputs = self.processor(raw_image, text, return_tensors="pt").to(self.device)

                out = self.model.generate(**inputs, num_beams=3)
                return {'description': self.processor.decode(out[0], skip_special_tokens=True)}

            self.classification_API = 'http://127.0.0.1:5000/predict'

        else:
            if classification_API != '':
                self.classification_API = input('Paste in your classifcation URL')
            else:
                self.classification_API = classification_API

    def classify(self, local_image_url) -> str:
        img_bytes = Image.open(local_image_url).convert('RGB').tobytes()

        response = requests.post(self.classification_API,
                                 data=img_bytes,
                                 headers={'Content-Type': 'image/jpg'})
        return response

    def start_server(host='127.0.0.1', port=5000):
        if CONFIG_run_local:
            import uvicorn
            uvicorn.run(app, port=5000)
