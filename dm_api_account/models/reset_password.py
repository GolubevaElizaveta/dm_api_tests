from __future__ import annotations

from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: Optional[str] = Field(..., description="Логин")
    email: Optional[str] = Field(..., description="Email")