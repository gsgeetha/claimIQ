from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from src.common.enums import ClaimStatus


class ClaimCreate(BaseModel):
    policy_number: str
    incident_date: date
    claim_amount: Decimal


class ClaimUpdate(BaseModel):
    status: ClaimStatus
    approved_amount: Decimal | None = None


class ClaimResponse(BaseModel):
    id: int
    claim_number: str
    policy_number: str
    incident_date: date
    claim_amount: Decimal
    approved_amount: Decimal | None
    status: ClaimStatus

    model_config = {"from_attributes": True}
