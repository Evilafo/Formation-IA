from fastapi import FastAPI, requests
from psutil import users
from pydantic import BaseModel
from typing import Optional



app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "MON API PERSO"}

users=[
     {"id": 1, "name": "Alice", "email": "alice@example.com"},
     {"id": 2, "name": "Bob", "email": "bob@example.com"},
     {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
     {"id": 4, "name": "David", "email": "david@example.com"},
     {"id": 5, "name": "Eve", "email": "eve@example.com"}
]
@app.get("/users")
def get_users():
    return users
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "Utilisateur non trouvé"}

    
class UserUpdate(BaseModel):
    name: Optional[str] = None 
    email: Optional[str] = None
    
class UserCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            del users[i]
            return {"message": "Utilisateur supprimé"}
    return {"error": "Utilisateur non trouvé"}

@app.post("/users")
def create_user(user: UserCreate):
    new_id = max(user["id"] for user in users) + 1
    new_user = {"id": new_id, "name": user.name, "email": user.email}
    users.append(new_user)
    return new_user

@app.put("/users/{user_id}")
def modify_user(user_id: int, user_update: UserUpdate):
    for u in users:
        if u["id"] == user_id:
            if user_update.name is not None:
                u["name"] = user_update.name
            if user_update.email is not None:
                u["email"] = user_update.email
            return u
    return {"error": "Utilisateur non trouvé"}

@app.patch("/users/{user_id}")
def partial_update_user(user_id: int, user_update: UserUpdate):
    for u in users:
        if u["id"] == user_id:
            if user_update.name is not None:
                u["name"] = user_update.name
            if user_update.email is not None:
                u["email"] = user_update.email
            return u
    return {"error": "Utilisateur non trouvé"}