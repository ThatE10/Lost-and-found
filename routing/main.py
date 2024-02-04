# main.py
import os
import shutil

from fastapi import FastAPI, File, Form, UploadFile
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import jinja2
from models import User
from utils import validate_phone, validate_email
import json
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("./static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")
IMAGE_FILE_PATH = './images/'
SUBMISSION_FILE_PATH = './submissions/'
os.makedirs(IMAGE_FILE_PATH, exist_ok=True)
os.makedirs(SUBMISSION_FILE_PATH, exist_ok=True)

id = 0


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submitform")
async def submit_form(
        request: Request,
        name: str = Form(),
        location: str = Form(),
        phone: str = Form(),
        email: str = Form(),
        photo: UploadFile = File(...)
):
    # import the global id#
    global id

    # Validate phone and email
    if not validate_phone(phone):
        return templates.TemplateResponse("error.html", {"request": request, "message": "Invalid phone number"})

    if not validate_email(email):
        return templates.TemplateResponse("error.html", {"request": request, "message": "Invalid email"})

    # Save photo

    ext = photo.filename.split('.')[-1]
    new_filename = f"{id}.{ext}"
    file_path = IMAGE_FILE_PATH + new_filename

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        print(f"Image saved to {file_path}")

    except Exception as e:
        print("Error saving image:", e)
        return {"error": "Unable to save image"}

    # Save submission as JSON
    user = User(
        name=name,
        location=location,
        phone=phone,
        email=email,
        id=id
    )

    user_json = json.dumps(user.dict())
    submission_file_path = SUBMISSION_FILE_PATH + f"{id}.json"
    with open(submission_file_path, "w") as f:
        f.write(user_json)

    id += 1

    return templates.TemplateResponse("success.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
