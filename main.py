import traceback
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

"""
todos = [{"title": "Introduction to Python",
          "description": "Wonderful Todo about Python", "author": "BO"}]
"""

from dbconfig.config import Base, engine, get_session
from models.todo import Todo  # wichtig: alle Models importieren
from models.user import User

Base.metadata.create_all(bind=engine)


class TodoCreate(BaseModel):
    title: str
    description: str
    user_id:int


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id:int

    class Config:
        orm_mode = True


session = next(get_session())


@app.get("/Todos",response_model=list[TodoResponse])
def get_todos() -> list[TodoResponse]|dict:
    try:
        todo_query = session.query(Todo)
        todos = todo_query.all()
        print(f"{todos=}")
        todos_responses = [*todos]
        print(f"{todos_responses=}")
        return todos_responses
    except Exception as ex:
        print("Fehler beim Laden der Todos:")
        traceback.print_exc()
        return {"error": str(ex)}


@app.post("/Todos", response_model=TodoResponse)
def create_Todo(todo_create: TodoCreate) -> TodoResponse:
    todo = Todo(title=todo_create.title,
                description=todo_create.description,user_id=todo_create.user_id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    # Todos.append(Todo.model_dump())
    todo_response = TodoResponse(id=todo.id, title=todo.title,
                                 description=todo.description
                                 ,user_id=todo.user_id)
    return todo_response


@app.put("/Todos/{id}",response_model=TodoResponse)
def put_Todo(id: int, todo_create: TodoCreate) -> TodoResponse:
    todo = session.query(Todo).filter(id == Todo.id).first()
    todo.title = todo_create.title
    todo.description = todo_create.description
    users=session.query(User).all()
    user_ids=[user.id for user in users]
    if todo_create.user_id in user_ids:
        todo.user_id=todo_create.user_id
    session.add(todo)
    session.commit()
    session.refresh(todo)
    todo_response=TodoResponse(id=todo.id,title=todo.title,description=todo.description,
                 user_id=todo.user_id)
    return todo_response


@app.get("/Todos/{id}")
def get_Todo(id: int) -> TodoCreate:
    todo = session.query(Todo).filter(id == Todo.id).first()
    print(f"{todo=}")
    todoCreate = TodoCreate(title=todo.title,
                            description=todo.description
                            ,user_id=todo.user_id)
    return todoCreate


@app.delete("/Todos/{id}")
def delete_Todo(id: int) -> None:
    todo = session.query(Todo).filter(id == Todo.id).first()
    session.delete(todo)
    session.commit()


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str


@app.get("/users", response_model=list[UserResponse]|dict)
def get_users():
    try:
        users = session.query(User).all()
        users_response = [*users]
        return users_response
    except Exception as ex:
        return ex.__dict__



@app.post("/users", response_model=UserResponse)
def create_user(user_create: UserCreate):
    user = User(name=user_create.name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(id=user.id, name=user.name )

@app.delete("/users/{id}")
def delete_user(id:int)->str:
    user:Optional[User]=session.query(User).filter(User.id==id).first()
    if user is not None:
        session.delete(user)
        session.commit()
        return f"User with {user.id} deleted"
    else:
        return f"User with {id} not in the database"


if __name__ == "__main__":
    pass
