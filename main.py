
import databases, sqlalchemy, uuid, datetime
from fastapi import FastAPI 

from pydantic import BaseModel, Field

from typing import List
## Postgres Database
DATABASE_URL = "postgresql://postgres:password@localhost:5432/db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key = True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("gender", sqlalchemy.CHAR),
    sqlalchemy.Column("create_at", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.CHAR),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

## Models
class Userlist(BaseModel):
    id: str
    username:str
    password:str
    first_name : str
    last_name: str
    gender: str
    create_at:str
    status : str

class UserEntry(BaseModel):
    username:str = Field(..., example="potinejj")
    password:str = Field(..., example="potinejj")
    first_name : str = Field(..., example="potine")
    last_name: str = Field(..., example="omar")
    gender: str = Field(..., example="M")


app1 = FastAPI()
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model = List[Userlist])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.post("/users", response_model = Userlist)
async def register_user(user: UserEntry):
    gID = str(uuid.uuid1())
    gDate = str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username   = user.username,
        password   = user.password,
        first_name = user.first_name,
        last_name  = user.last_name, 
        gender     = user.gender,
        create_at = gDate,
        status     = "1"

    )
    
    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at": gDate,
        "status":"1"
    }