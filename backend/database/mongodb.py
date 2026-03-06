from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://httrqd:httrqd@cluster0.vf8xv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

client = AsyncIOMotorClient(MONGO_URI)

db = client["dss_rental"]

users_collection = db["users"]
rentals_collection = db["rentals"]
criteria_collection = db["criteria"]
ahp_matrix_collection = db["ahp_matrices"]
ahp_weights_collection = db["ahp_weights"]
recommendations_collection = db["recommendations"]