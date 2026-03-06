from fastapi import APIRouter, Depends

from database.mongodb import rentals_collection
from services.embedding_service import EmbeddingService
from services.ranking_service import RankingService
from services.auth_dependency import get_current_user

router = APIRouter(prefix="/rentals")

@router.post("/search")

async def search_rentals(
    data: dict,
    user = Depends(get_current_user)
):

    query = data["query"]
    max_price = data["max_price"]
    min_area = data["min_area"]
    weights = data["weights"]

    # tạo embedding từ query
    query_embedding = EmbeddingService.generate_embedding(query)

    # filter MongoDB
    rentals = await rentals_collection.find(
        {
            "price": {"$lte": max_price},
            "area": {"$gte": min_area}
        }
    ).to_list(100)

    # ranking
    ranked = RankingService.rank(
        rentals,
        weights,
        query_embedding
    )

    return ranked