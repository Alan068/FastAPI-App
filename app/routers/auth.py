from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from uuid import uuid4
from app.settings import settings


# print(settings,"555555")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()  # '|'is bitwise OR op in py, but means logical OR in sqlalchemy.
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        user_id=uuid4(),
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="user"   # By default given role as 'user' when registers.
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
