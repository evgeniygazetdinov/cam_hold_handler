from typing import List

import uvicorn
import sqlalchemy
from databases import Database
from fastapi import FastAPI
from pydantic import BaseModel, Json


DATABASE_URL = "sqlite:///test.db"


app = FastAPI()

# database
database = Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()

api_flow_json = sqlalchemy.Table(
    "my_data",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("customer_name", sqlalchemy.String),
    # sqlalchemy.Column("entities", sqlalchemy.JSON),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

# pydantic

class MyData(BaseModel):
    id: int
    customer_name: str
    # entities: Json

    class Config:
        orm_mode = True


# events

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# route handlers

@app.get("/")
def home():
    return "Hello, World!"


@app.get("/seed")
async def seed():
    query = api_flow_json.insert().values(
        customer_name="ABC",
    )
    record_id = await database.execute(query)
    return {"id": record_id}


@app.get("/get", response_model=List[MyData])
async def get_data():
    query = api_flow_json.select()
    record_id = await database.execute(query)
    return record_id

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8008, debug=True)