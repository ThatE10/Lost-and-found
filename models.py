from pydantic import BaseModel


class User(BaseModel):
    name: str
    location: str
    phone: str
    email: str
    id: int
