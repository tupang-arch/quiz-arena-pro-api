from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .database import SessionLocal
from .models import User
from .settings import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token: missing sub")

        # sub poate fi string -> îl convertim la int dacă e user_id
        try:
            user_id = int(sub)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token: sub is not int")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        # ca să vezi clar eroarea în terminal:
        print("🔥 ERROR in get_current_user:", repr(e))
        raise HTTPException(status_code=500, detail="Internal server error")
    from fastapi import Depends, HTTPException, status
from .models import User

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user