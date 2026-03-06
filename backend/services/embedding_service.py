from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str):

        embedding = model.encode(text)

        return embedding.tolist()