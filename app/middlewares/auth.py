from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.user import User
from app.settings import settings
from uuid import UUID


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"Decoded Token: {payload}")  # debugging
        user_id_str: str = payload.get("sub")   # Check user_id and role exists
        role: str = payload.get("role")

        if not user_id_str or not role:
            raise HTTPException(status_code=401, detail="Invalid token")

        return UUID(user_id_str), role    # Converts sub (user_id) to uid
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID format")

# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:


def get_current_user(token: str = Header(None), db: Session = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    print(f"Received Token: {token}")        # Debugging

    user_id, role = decode_token(token)

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    print(f"Authenticated User: {user.username}, Role: {user.role.value}")       # Debugging
    return user


def manager_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.value not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user


def admin_required(current_user: User = Depends(get_current_user)) -> User:
    print(f"Admin access for: {current_user.username}, Role: {current_user.role}")        # Debugging
    if  current_user.role.value != "admin":                                             # if current_user.role != "admin":  I'm using enum, but if db storing as str, str(current_user.role).lower() != "admin"
        print("Access Denied: User is not an admin")                                      # Debugging
        raise HTTPException(status_code=403, detail="Not authorized")
    print("Access Granted: Admin detected")                                           # Debugging
    return current_user




# def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id_str: str = payload.get("sub")  # user_id (UUID as string)
#         if user_id_str is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         user_id = UUID(user_id_str)  # Converting sub to UUID
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     except ValueError:
#         raise HTTPException(status_code=401, detail="Invalid user ID format")

#     user = db.query(User).filter(User.user_id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user


# def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
#     if current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Not authorized")
#     return current_user
