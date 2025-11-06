from fastapi import FastAPI, Path, Body, status, Header, Response
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uuid
#обьект приложения

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())

people = [Person("Argenta", 11241), Person("Gerant", 23652), Person("Velskud", 432632)]

def find_person(id):
    for person in people:
        if person.id == id:
            return person
        return None
    
app = FastAPI()

@app.get("/")
async def main():
    return FileResponse("public/index.html")

@app.get("/api/users")
def get_people():
    return people

@app.get("/api/users/{id}")
def get_person(id):
    person = find_person(id)
    print(person)
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    return person

@app.post("/api/users")
def create_person(data = Body()):
    person = Person(data["name"], data["age"])
    people.append(person)
    return person

@app.put("/api/users")
def edit_person(data = Body()):
    person = find_person(data["id"])
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    person.age = data("age")
    person.name = data("name")
    return person

@app.delete("/api/users/{id}")
def delete_person(id):
    person = find_person(id)

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    people.remove(person)
    return person
# @app.get("/users/{id}")
# def users(id):
#     return {"user_id": id}

# @app.get("/users/{name}")
# def users(name:str  = Path(min_length=3, max_length=20)):
#     return {"name": name}

# @app.get('/text')
# def printInfo(age: int, name: str):
#     return {"age": age, "name": name}

# @app.get("/error", status_code=404)
# def notFound():
#     return {"error": "Error 404"}

# @app.get("/old")
# def old():
#     return RedirectResponse("/new")

# @app.get("/new")
# def new():
#     return PlainTextResponse("Новая страница")

# app.mount("/static", StaticFiles(directory="public"))

# @app.get("/")
# def root():
#     return FileResponse("public/index.html")

# @app.post("/hello")
# def hello(name:str  = Body(embed=True, min_length=3, max_length=20), 
#             age: int = Body(embed=True, ge=18, lt=111)):
#     return {"message": f"{name}, ваш возраст - {age}"}

# class Person(BaseModel):
#     name: str = Field(default="Undefined", min_length=3, max_length=20)
#     age: int = Field(default=18, ge=18, lt=111)
#     # name: str
#     # age: int | None = None

# @app.get("/")
# def root():
#     return FileResponse("public/index.html")

# @app.post("/hello")
# def hello(person: Person):
#     return {"message": f"Привет, {person.name}, твой возраст - {person.age}"}

# @app.post("/hello")
# def hello(person: Person):
#     if person.age == None:
#         return {"message": f"Привет, {person.name}"}
#     else:
#         return {"message": f"Привет, {person.name}, твой возраст - {person.age}"}

# @app.post("/hello")
# def hello(people:list[Person]):
#     return {"message": people}

# Отправка заголовков
@app.get("/")
def root():
    data = "Hello"
    return Response(content=data, media_type="text/plain", headers={"Secret-Code" : "123459"})
# Для примера в данном случае клиенту отправляется кастомный заголовок "Secret-Code" со значением "123459":
@app.get("/")
def root(response: Response):
    response.headers["Secret-Code"] = "123459"
    return {"message": "Hello"}
# Данный атрибут фактически представляет словарь, где ключи - названия заголовков:
# Получение заголовков

@app.get("/")
def root(user_agent: str = Header()):
    return {"User-Agent": user_agent}
# def root(secret_code: str | None = Header(default=None)):
#     return {"Secret-Code": secret_code}
