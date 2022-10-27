from db import SessionLocal

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import uvicorn
#import crud to give access to the operations that we defined
import crud2 as crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()



#define endpoint
@app.get("/create_friend")
def create_friend(first_name:str, last_name:str, age:int, db:Session = Depends(get_db)):
    friend = crud.create_friend(db=db, first_name=first_name, last_name=last_name, age=age)
    return {"friend": friend}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8009, debug=True)