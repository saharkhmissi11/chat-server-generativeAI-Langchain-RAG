from pydantic import BaseModel

class Document(BaseModel):
    id: int
    description: str
    url: str
