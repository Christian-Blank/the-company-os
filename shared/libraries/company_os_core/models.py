from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BaseDocument(BaseModel):
    """Base model for all markdown documents"""

    title: str
    version: str = "1.0"
    status: str
    owner: str
    last_updated: datetime
    parent_charter: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
