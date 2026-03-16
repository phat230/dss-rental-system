import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.mongodb import users_collection
from services.auth_service import hash_password


async def create_admin():

    email = "phay123321@gmail.com"

    existing = await users_collection.find_one(
        {"email": email}
    )

    if existing:
        print("Admin already exists")
        return

    admin_user = {

        "name": "Phay Admin",
        "email": email,
        "password": hash_password("123456789"),
        "role": "admin"

    }

    result = await users_collection.insert_one(admin_user)

    print("Admin created:", result.inserted_id)


if __name__ == "__main__":
    asyncio.run(create_admin())