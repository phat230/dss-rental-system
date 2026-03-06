from fastapi import APIRouter
from database.mongodb import rentals_collection
from services.embedding_service import EmbeddingService
from services.ranking_service import RankingService

router = APIRouter()

@router.post("/rentals/search")

async def search_rentals(data: dict):

    query = data["query"]
    max_price = data["max_price"]
    min_area = data["min_area"]
    weights = data["weights"]

    query_embedding = EmbeddingService.generate_embedding(query)

    rentals = await rentals_collection.find(
        {
            "price": {"$lte": max_price},
            "area": {"$gte": min_area}
        }
    ).to_list(100)

    ranked = RankingService.rank(rentals, weights, query_embedding)

    return ranked