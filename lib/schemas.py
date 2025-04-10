from datetime import datetime
from typing import Optional, Dict
from uuid import UUID

from pydantic import BaseModel, Field

class User(BaseModel):
    type: str
    recipient: str
    content: str
    variables: Dict = Field(default_factory=dict)
