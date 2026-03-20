from fastapi import APIRouter, Depends
from database.mongodb import rentals_collection, users_collection
from services.auth_dependency import admin_required
from bson import ObjectId

router = APIRouter(prefix="/admin")

# =============================
# 🏠 RENTALS CRUD
# =============================

@router.post("/add-rental")
async def add_rental(data: dict, user=Depends(admin_required)):
    await rentals_collection.insert_one(data)
    return {"message": "Rental added"}


@router.get("/rentals")
async def get_rentals(user=Depends(admin_required)):
    rentals = await rentals_collection.find().to_list(100)
    for r in rentals:
        r["_id"] = str(r["_id"])
    return rentals


@router.put("/update-rental/{id}")
async def update_rental(id: str, data: dict, user=Depends(admin_required)):
    await rentals_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return {"message": "Updated"}


@router.delete("/delete-rental/{id}")
async def delete_rental(id: str, user=Depends(admin_required)):
    await rentals_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"}


# =============================
# 👤 USERS
# =============================

@router.get("/users")
async def get_users(user=Depends(admin_required)):
    users = await users_collection.find().to_list(100)
    for u in users:
        u["_id"] = str(u["_id"])
    return users


@router.delete("/delete-user/{id}")
async def delete_user(id: str, user=Depends(admin_required)):
    await users_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "User deleted"}