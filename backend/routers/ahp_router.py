from fastapi import APIRouter
from models.ahp_matrix import AHPMatrix
from services.ahp_service import AHPService

router = APIRouter()

@router.post("/ahp/calculate")

def calculate_ahp(data: AHPMatrix):

    weights, CR = AHPService.calculate_weights(data.matrix)

    return {
        "weights": weights,
        "CR": CR
    }