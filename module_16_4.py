from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

#  GET
@app.get("/users")  #  На запрос /users выводим словарь users
async def get_users() -> List[User]:
    return users
#  POST
@app.post("/user/{username}/{age}")  #  На запрос /user/{username}/{age} вносим нового пользователя
async def new_user(username: Annotated[str, Path(min_length=2,                     # Минимальная длина username
                                               max_length=20,                      # Максимальная длина username
                                               description="Enter your username",  # описание для ввода username
                                               examples="User")],                   # пример
                   age: Annotated[int, Path(ge=10,                    # age только больше или равен 10
                                            le=100,                   # age не более 100
                                            description="Enter age",  # описание для ввода age
                                            examples=24)]) ->str:            # пример

    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return str(new_user)
    raise HTTPException(status_code=404, detail="User was not found")


#  PUT
@app.put("/user/{user_id}/{username}/{age}")
def edit_user(
    user_id: Annotated[int, Path(ge=1,
                                 le=50,
                                 description="Enter user_id",
                                 examples=1)],
    username: Annotated[str, Path(min_length=2,
                                  max_length=20,
                                  description="Enter your username",
                                  examples="User")],
    age: Annotated[int, Path(ge=10,
                             le=100,
                             description="Enter age",
                             examples=24)]) ->str:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            raise HTTPException(status_code=404, detail="User was not found")
            return str(user)

#  DELETE
@app.delete("/user/{user_id}")
def del_user(
        user_id: Annotated[int, Path(
            ge=1,
            le=50,
            description="Enter user_id",
            examples=1)]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")


"""
  Запускаем в терминале PyCharm
python -m uvicorn module_16_4:app  
      где module_16_4 - имя файла, 
      app - объект FastAPI() в коде module_16_4.py

Для входа в FastAPI Swagger UI вводим http://127.0.0.1:8000/docs
"""