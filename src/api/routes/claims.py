from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.claim import (
    ClaimCreate,
    ClaimUpdate,
    ClaimResponse,
)
from src.services.claim_service import ClaimService

router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
)


@router.post(
    "/",
    response_model=ClaimResponse,
)
def create_claim(
    payload: ClaimCreate,
    db: Session = Depends(get_db),
):
    return ClaimService.create_claim(
        db,
        payload,
    )


@router.get(
    "/",
    response_model=list[ClaimResponse],
)
def get_claims(
    db: Session = Depends(get_db),
):
    return ClaimService.get_claims(db)


@router.get(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
):
    return ClaimService.get_claim(
        db,
        claim_id,
    )


@router.put(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def update_claim(
    claim_id: int,
    payload: ClaimUpdate,
    db: Session = Depends(get_db),
):
    return ClaimService.update_claim(
        db,
        claim_id,
        payload,
    )


@router.delete(
    "/{claim_id}",
)
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db),
):
    ClaimService.delete_claim(
        db,
        claim_id,
    )

    return {"message": "Claim deleted successfully"}
