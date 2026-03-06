from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "SECRET_DSS_RENTAL"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(password, hashed):

    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token