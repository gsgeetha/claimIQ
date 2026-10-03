from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserRead, UserUpdate
from src.services.user_service import *

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    validate_unique_email(payload.email, db)
    validate_unique_username(payload.username, db)

    user = User(username=payload.username, email=payload.email, role=payload.role)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(user_id, db)


@router.put("/{user_id}")
def update_existing_user(
    user_id: int, payload: UserUpdate, db: Session = Depends(get_db)
):
    return update_user(user_id, payload, db)


@router.delete("/{user_id}", status_code=204)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
