from pydantic import BaseModel
from typing import List

class Rental(BaseModel):

    title: str
    description: str
    price: float
    area: float
    location: str
    security: float
    amenities: float
    embedding: List[float] = []
    image_url: str = ""