from sentence_transformers import SentenceTransformer

model = None

class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str):
        global model

        if model is None:
            model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        embedding = model.encode(text)
        return embedding.tolist()