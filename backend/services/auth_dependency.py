from fastapi import Header, HTTPException, Depends
from jose import jwt

SECRET_KEY = "SECRET_DSS_RENTAL"
ALGORITHM = "HS256"


def get_current_user(token: str = Header(...)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def admin_required(user = Depends(get_current_user)):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return user