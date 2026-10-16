from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.policy import PolicyCreate, PolicyRead, PolicyUpdate

from src.services.policy_service import *

router = APIRouter(prefix="/api/v1/policies", tags=["Policies"])


@router.post("", response_model=PolicyRead)
def create_new_policy(payload: PolicyCreate, db: Session = Depends(get_db)):
    return create_policy(payload, db)


@router.get("", response_model=list[PolicyRead])
def list_policies(db: Session = Depends(get_db)):
    return get_policies(db)


@router.get("/{policy_id}", response_model=PolicyRead)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    return get_policy_by_id(policy_id, db)


@router.put("/{policy_id}", response_model=PolicyRead)
def update_existing_policy(
    policy_id: int, payload: PolicyUpdate, db: Session = Depends(get_db)
):
    return update_policy(policy_id, payload, db)


@router.delete("/{policy_id}")
def remove_policy(policy_id: int, db: Session = Depends(get_db)):
    return delete_policy(policy_id, db)
