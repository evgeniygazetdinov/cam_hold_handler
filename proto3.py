from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, models, schemas



app = FastAPI()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# route handlers

@app.get("/")
def home():
    return "Hello, World!"


# @app.get("/seed")
# async def seed():
#     query = api_flow_json.insert().values(
#         customer_name="ABC",
#     )
#     record_id = await database.execute(query)
#     return {"id": record_id}

@app.get("/users/{customer_name}", response_model=schemas.MyData)
def read_user(customer_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, customer_name=customer_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8008, debug=True)