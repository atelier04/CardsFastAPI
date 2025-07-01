from pydantic import (BaseModel, EmailStr, StringConstraints,
                      field_validator, field_serializer)
from pydantic import validator


class Person(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value):

        if len(value) < 5:
            raise ValueError("Password must be greater 5 ")
        return value




p1 = Person(name="Tom", email="tom@gmail.com", password="rr777777")
print(p1.model_dump(mode="json"))
print(Person.model_validate(p1))