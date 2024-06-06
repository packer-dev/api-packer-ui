from pydantic import BaseModel

class Role(BaseModel):
    role: str
    content: str