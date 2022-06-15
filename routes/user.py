from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from bson import ObjectId
from passlib.hash import sha256_crypt
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', response_model=list[User], tags=["Users"])
def get_users():
    return usersEntity(conn.TrainDB.Users.find())

@user.get('/users/{id}', response_model=User, tags=["Users"])
def get_user(id: str):
    return userEntity(conn.TrainDB.Users.find_one({"_id":ObjectId(id)}))

@user.post('/users', response_model=User, tags=["Users"])
def create_user(user: User):
    new_user = dict(user)  
    del new_user["id"]
    new_user["password"]=sha256_crypt.encrypt(new_user["password"])
    id=conn.TrainDB.Users.insert_one(new_user).inserted_id
    user=conn.TrainDB.Users.find_one({"_id":id})
    return userEntity(user)

@user.put('/users/{id}', response_model=User, tags=["Users"])
def update_user(id: str, user: User):
    actual_user=dict(user)
    del actual_user["id"]
    actual_user["password"]=sha256_crypt.encrypt(actual_user["password"])
    conn.TrainDB.Users.find_one_and_update({"_id":ObjectId(id)}, {"$set":actual_user})
    return userEntity(conn.TrainDB.Users.find_one({"_id":ObjectId(id)}))

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: str):
    conn.TrainDB.Users.find_one_and_delete({"_id":ObjectId(id)})
    return Response(status_code=HTTP_204_NO_CONTENT)