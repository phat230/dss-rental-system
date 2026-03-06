import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongodb import rentals_collection
from services.embedding_service import EmbeddingService


async def generate_embeddings():

    rentals = await rentals_collection.find().to_list(1000)

    for rental in rentals:

        text = rental.get("description", "")

        embedding = EmbeddingService.generate_embedding(text)

        await rentals_collection.update_one(
            {"_id": rental["_id"]},
            {"$set": {"embedding": embedding}}
        )

        print("Updated:", rental.get("title", "unknown"))


if __name__ == "__main__":
    asyncio.run(generate_embeddings())