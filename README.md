# Image Classifier for Lost & Founds with Web UI

***Project Description***: Image Classifier for Lost & Found's with WebUI
Major issue within lost and founds that deal with hundreds of objects everyday is that someone has to write a high qualitity description of object and provide a classification and additional details.  This project sought to provide an easy way to classify and categorize the object for easy information retrieval with.  

This project serves as a tutorial for members of Charlotte AI Research (CAIR) and Charlotte Hack to learn more about implementation of AI models within real world applications.  This project will teach members the basics of using  Dev Ops, Google Collab, Ngrok FastAPI, HuggingFace, PyUnittests, and File Read and writes.  

# Tutorial
Setting up your environment is key to your success!  In this tutorial we will be mainly using Python 3.11 (Current version is 3.12) please download the [previous version](https://www.python.org/downloads/release/python-3110/) to use this project.

Note I will use PyCharm for the entirety of the project, if you don't feel comfortably creating virtual environments and customising runtime please use [PyCharm](https://www.jetbrains.com/pycharm/download/download-thanks.html?) as well.

This tutorial will assume you are using Google Colab to run the model incase your machine can't handle the heavy models


#TODO Ethan add the VENV tutorial for pycharm :D


## This project is separated into 3 parts:
- HuggingFace Implementation
- Local & Global ML model implementation
- FastAPI Implementation

## HuggingFace Models
Hugging Face is a company and an open-source platform that specializes in natural language processing (NLP) and machine learning. The company is renowned for its contributions to the development and distribution of state-of-the-art models for various NLP tasks. One of its notable achievements is the creation of the Transformers library, which serves as a comprehensive repository for pre-trained language models.

This section for reference will lay the ground works to create your own [ml_model.classification]() 

**Choosing the model**:
I decided to go with [FuseCap](https://huggingface.co/noamrot/FuseCap_Image_Captioning) for its high fidelity output and ease of use.  Feel free to look up other `Image Captioning` AI models if you want to customise it a little! 

To start using this copy and past the code into your [Colab Notebook](https://colab.new)
```python
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

device = torch.device('cuda'  if torch.cuda.is_available()  else  'cpu')
processor = BlipProcessor.from_pretrained("noamrot/FuseCap")
model = BlipForConditionalGeneration.from_pretrained("noamrot/FuseCap").to(device)

img_url = ''
raw_image = ''

if  not img_url:
	img_url = 'https://huggingface.co/spaces/noamrot/FuseCap/resolve/main/bike.jpg'
	raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
else:
	raw_image = Image.open(img_url).convert('RGB')


text = "a picture of "
inputs = processor(raw_image, text, return_tensors="pt").to(device)
out = model.generate(**inputs, num_beams = 3)
print(processor.decode(out[0], skip_special_tokens=True))
```
[Google Colab Basics Tutorial](https://www.youtube.com/watch?v=RLYoEyIHL6A)

Running this the first time will give you a description of the [Red Motor Cycle Image](https://huggingface.co/spaces/noamrot/FuseCap/resolve/main/bike.jpg) if you want to use your own upload the your own jpg to the folder folder and paste the local file path url into `img_url` 

This is great now you have your own machine learning model that works!  Congrats!  But now how do we start integrating this into our application.  We will want to be able to access this through something called an [API](https://www.youtube.com/watch?v=0RS9W8MtZe4) that runs on the Google Colab notebook.

We will use something called 'Ngrok' to allow you to connect your local server to the internet fastly and easily.  [Create an account](https://dashboard.ngrok.com/signup) and grab your auth key

Create a new [+Code] block and paste this code into it
```python
!pip install  fastapi
!pip install  nest-asyncio pyngrok uvicorn
!pip install  typing-extensions 
!pip install  starlette
!pip install  python-multipart
from io import BytesIO
import os
#from typing_extensions import Buffer 

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/predict")
def predict(image: bytes = File(...)):
      raw_image = Image.open(BytesIO(image))
      text = "a picture of "
      inputs = processor(raw_image, text, return_tensors="pt").to(device)

      out = model.generate(**inputs, num_beams=3)
      return {'description': processor.decode(out[0], skip_special_tokens=True)}

import nest_asyncio
from pyngrok import ngrok
import uvicorn

ngrok.set_auth_token(["YOUR AUTH TOKEN"])

ngrok_tunnel = ngrok.connect(5000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=5000)
```

When you run this block it will output a Public URL similar to '[https://5919-34-125-248-184.ngrok-free.app](https://5919-34-125-248-184.ngrok-free.app)' this will be your endpoint for predictions

*Next we will create an application that is able to access this endpoint on your local machine*

Create a new project and create a folder called ML_endpoint then create a file called predict.py within that folder
