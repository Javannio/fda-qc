from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime

class RecallRecord(BaseModel):
    recall_number: str
    status: str
    classification: str
    state: Optional[str] = None
    country: str
    recalling_firm: str
    product_description: str
    reason_for_recall: str
    voluntary_mandated: str
    recall_initiation_date: str
    report_date: str
    termination_date: Optional[str] = None

    @field_validator('classification')
    @classmethod
    def valid_classification(cls, v):
        allowed = {'Class I', 'Class II', 'Class III'}
        if v not in allowed:
            raise ValueError(f'classification must be one of {allowed}, got {v}')
        return v

    @field_validator('status')
    @classmethod
    def valid_status(cls, v):
        allowed = {'Terminated', 'Ongoing', 'Completed'}
        if v not in allowed:
            raise ValueError(f'status must be one of {allowed}, got {v}')
        return v

    @field_validator('recall_initiation_date', 'report_date', 'termination_date')
    @classmethod
    def valid_yyyymmdd_date(cls, v):
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y%m%d')
        except ValueError:
            raise ValueError(f'date must be YYYYMMDD format, got {v}')
        return v

    @model_validator(mode='after')
    def state_country_consistency(self):
        if self.country == 'United States' and self.state is None:
            raise ValueError("US recall missing state")
        return self

    @model_validator(mode='after')
    def status_termination_consistency(self):
        if self.status == 'Ongoing' and self.termination_date is not None:
            raise ValueError(f"logical inconsistency: status is 'Ongoing' but termination_date is set ({self.termination_date})")
        if self.status == 'Terminated' and self.termination_date is None:
            raise ValueError("logical inconsistency: status is 'Terminated' but termination_date is missing")
        return self
