from fastapi import APIRouter, UploadFile, File
import pandas as pd
from database.mongodb import rentals_collection

router = APIRouter(prefix="/import")

@router.post("/excel")
async def import_excel(file: UploadFile = File(...)):

    df = pd.read_excel(file.file)

    data_list = df.to_dict(orient="records")

    for item in data_list:

        # 🔥 lấy tên ảnh từ excel
        image_name = item.get("image", "")

        # 🔥 auto gán đường dẫn ảnh
        item["image_url"] = f"http://127.0.0.1:8000/uploads/{image_name}"

        # embedding rỗng
        item["embedding"] = []

        await rentals_collection.insert_one(item)

    return {"message": "Import thành công"}