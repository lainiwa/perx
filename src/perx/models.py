from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class Task(BaseModel):
    n: int
    d: float
    n1: float = 0
    interval: float = 1


class Result(Task):
    current_val: Optional[float] = None
    started: Optional[datetime] = None
    times_applied = 0

    @validator('started', pre=True, always=True)
    def set_started_now(cls, v):
        return v or datetime.now()

    @validator('current_val', pre=True, always=True)
    def default_current_val(cls, v, *, values, **kwargs):
        return v or values['n1']
