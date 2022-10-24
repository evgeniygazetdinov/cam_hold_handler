from typing import List, Union

from pydantic import BaseModel


class MyData(BaseModel):
    id: int
    customer_name: str
    # entities: Json

    class Config:
        orm_mode = True
