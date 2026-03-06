from fastapi import APIRouter
from database.mongodb import users_collection
from services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(data: dict):

    existing = await users_collection.find_one(
        {"email": data["email"]}
    )

    if existing:
        return {"error": "Email already exists"}

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hash_password(data["password"]),
        "role": "user"
    }

    await users_collection.insert_one(user)

    return {"message": "User created"}


@router.post("/login")
async def login(data: dict):

    user = await users_collection.find_one(
        {"email": data["email"]}
    )

    if not user:
        return {"error": "User not found"}

    if not verify_password(
        data["password"],
        user["password"]
    ):
        return {"error": "Wrong password"}

    token = create_access_token({
        "user_id": str(user["_id"]),
        "role": user["role"]
    })

    return {
        "token": token,
        "role": user["role"],
        "name": user["name"]
    }