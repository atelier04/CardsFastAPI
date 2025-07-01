from pydantic import BaseModel, EmailStr, StringConstraints
from pydantic import validator


class Person(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        print(value)
        if len(value) < 5:
            raise ValueError("Password must be greater 5 ")
        return len(value)


p1 = Person(name="Tom", email="tom@gmail.com", password="rr")
