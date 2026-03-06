from pydantic import BaseModel
from typing import List

class AHPMatrix(BaseModel):

    matrix: List[List[float]]