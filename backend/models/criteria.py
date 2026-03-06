from pydantic import BaseModel

class Criteria(BaseModel):

    name: str
    description: str