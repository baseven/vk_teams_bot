from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class VacationType(str, Enum):
    ANNUAL_PAID = "annual_paid"
    UNPAID = "unpaid"
    SICK_LEAVE = "sick_leave"
    MATERNITY_OR_PATERNITY = "maternity_or_paternity"
    COMPASSIONATE = "compassionate"
    STUDY = "study"


class VacationStatus(str, Enum):
    PLANNED = "planned"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Vacation(BaseModel):
    vacation_type: VacationType = Field(..., description="Type of vacation (e.g., annual paid, unpaid, sick leave)")
    start_date: datetime = Field(..., description="Start date of the vacation")
    end_date: datetime = Field(..., description="End date of the vacation")
    status: VacationStatus = Field(...,
                                   description="Current status of the vacation (e.g., planned, approved, rejected)")
    vacation_id: Optional[str] = Field(None, description="Unique identifier for the vacation")
    request_date: Optional[datetime] = Field(None, description="Date when the vacation was requested")
    comment: Optional[str] = Field(None, description="Additional comments or notes related to the vacation")
    available_days: Optional[int] = Field(None, description="Current number of available days for this type of leave")
    approved_by: Optional[str] = Field(None, description="ID or name of the person who approved the vacation")

    class Config:
        use_enum_values = True
        validate_assignment = True


class Limit(BaseModel):
    vacation_type: VacationType = Field(..., description="Type of vacation (e.g., annual paid, unpaid, sick leave)")
    available_days: int = Field(..., description="Current number of available days for this type of vacation")

    class Config:
        validate_assignment = True
