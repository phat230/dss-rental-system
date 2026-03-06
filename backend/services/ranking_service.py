from .vector_service import VectorService

class RankingService:

    @staticmethod
    def rank(rentals, weights, query_embedding):

        results = []

        for rental in rentals:

            criteria_score = (
                weights[0] * (1 / rental["price"]) +
                weights[1] * rental["area"] +
                weights[2] * rental["security"]
            )

            similarity = VectorService.cosine_similarity(
                query_embedding,
                rental["embedding"]
            )

            final_score = criteria_score + similarity

            rental["score"] = final_score

            results.append(rental)

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:10]