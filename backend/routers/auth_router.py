from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from database.mongodb import users_collection
from services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- 1. ĐỊNH NGHĨA DATA MODELS (Chuẩn Doanh Nghiệp) ---
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr  # Tự động validate chuẩn email
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- 2. ENDPOINT ĐĂNG KÝ ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    # Kiểm tra email tồn tại
    existing = await users_collection.find_one({"email": data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email đã được sử dụng."
        )

    # Khởi tạo user document
    user_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "user"
    }

    await users_collection.insert_one(user_doc)
    return {"message": "Tài khoản đã được khởi tạo thành công."}

# --- 3. ENDPOINT ĐĂNG NHẬP ---
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: LoginRequest):
    # Tìm user trong DB
    user = await users_collection.find_one({"email": data.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy tài khoản với email này."
        )

    # Xác thực mật khẩu (Sử dụng try-except để chống crash do dữ liệu cũ)
    try:
        is_valid = verify_password(data.password, user.get("password", ""))
    except Exception:
        is_valid = False

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Mật khẩu không chính xác."
        )

    # Khởi tạo JWT Token (Sử dụng .get() để tránh KeyError nếu DB cũ thiếu trường)
    role = user.get("role", "user")
    name = user.get("name", "Unknown User")
    
    token = create_access_token({
        "user_id": str(user["_id"]),
        "role": role
    })

    return {
        "token": token,
        "role": role,
        "name": name
    }