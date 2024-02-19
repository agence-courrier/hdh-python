from fastapi import FastAPI, HTTPException
import uvicorn
import json
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


class Geolocalion(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geolocalion


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/")
def read_all_items():
    with open("database.json") as read_file:
        users_list = json.load(read_file)
        return users_list


@app.get("/users/{user_id}")
def read_item(user_id: int):
    with open("database.json") as read_file:
        users_list = json.load(read_file)
    filtered_user = [user for user in users_list if user["id"] == user_id]
    if len(filtered_user) != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return filtered_user[0]


@app.post("/user/")
def post_user(user: User):
    with open("database.json") as read_file:
        users_list = json.load(read_file)

    user_json = jsonable_encoder(user)
    users_list.append(user_json)

    with open("database.json", "w") as write_file:
        json.dump(users_list, write_file, indent=4)

    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
