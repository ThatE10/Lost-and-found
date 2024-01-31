# main.py

from fastapi import FastAPI, File, Form, UploadFile
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from models import User
from utils import validate_phone, validate_email
import json


app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
    global id
    # Validate phone and email
    if not validate_phone(phone):
        return templates.TemplateResponse("error.html", {"request": request, "message": "Invalid phone number"})

    if not validate_email(email):
        return templates.TemplateResponse("error.html", {"request": request, "message": "Invalid email"})

    # Save photo
    #
    filename = photo.filename
    ext = filename.split('.')[-1]
    new_filename = f"{id}.{ext}"
    file_path = f"images/{new_filename}"

    # Create User model
    user = User(
            name=name,
            location=location,
            phone=phone,
            email=email,
            id=id
                )

    # Save as JSON
    user_json = json.dumps(user.dict())
    with open(f"{id}.json", "w") as f:
        f.write(user_json)

    id += 1

    return templates.TemplateResponse("success.html", ...)