import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.claim import Claim
from src.models.policy import Policy
from src.common.enums import (
    ClaimStatus,
    PolicyStatus,
)
from src.schemas.claim import (
    ClaimCreate,
    ClaimUpdate,
)


class ClaimService:

    @staticmethod
    def create_claim(
        db: Session,
        payload: ClaimCreate,
    ):
        policy = (
            db.query(Policy)
            .filter(Policy.policy_number == payload.policy_number)
            .first()
        )

        if not policy:
            raise HTTPException(
                status_code=404,
                detail="Policy not found",
            )

        if policy.status != PolicyStatus.active:
            raise HTTPException(
                status_code=400,
                detail="Policy is not active",
            )
        if not (policy.start_date <= payload.incident_date <= policy.end_date):
            raise HTTPException(
                status_code=400,
                detail="Incident date is outside policy coverage period",
            )
        if payload.claim_amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Claim amount must be greater than zero",
            )

        claim = Claim(
            claim_number=f"CLM-{uuid.uuid4().hex[:8].upper()}",
            policy_id=policy.id,
            incident_date=payload.incident_date,
            claim_amount=payload.claim_amount,
            status=ClaimStatus.submitted,
        )

        db.add(claim)
        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def get_claim(
        db: Session,
        claim_id: int,
    ):
        claim = db.query(Claim).filter(Claim.id == claim_id).first()

        if not claim:
            raise HTTPException(
                status_code=404,
                detail="Claim not found",
            )

        return claim

    @staticmethod
    def get_claims(
        db: Session,
    ):
        return db.query(Claim).all()

    @staticmethod
    def update_claim(
        db: Session,
        claim_id: int,
        payload: ClaimUpdate,
    ):
        claim = db.query(Claim).filter(Claim.id == claim_id).first()

        if not claim:
            raise HTTPException(
                status_code=404,
                detail="Claim not found",
            )
        if payload.status == ClaimStatus.approved and payload.approved_amount is None:
            raise HTTPException(
                status_code=400,
                detail="Approved amount is required for approved claims",
            )
        if (
            payload.approved_amount is not None
            and payload.approved_amount > claim.claim_amount
        ):
            raise HTTPException(
                status_code=400,
                detail="Approved amount cannot exceed claim amount",
            )

        claim.status = payload.status
        claim.approved_amount = payload.approved_amount

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def delete_claim(
        db: Session,
        claim_id: int,
    ):
        claim = db.query(Claim).filter(Claim.id == claim_id).first()

        if not claim:
            raise HTTPException(
                status_code=404,
                detail="Claim not found",
            )

        db.delete(claim)
        db.commit()
