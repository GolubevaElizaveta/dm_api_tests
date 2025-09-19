from __future__ import annotations

from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: Optional[str] = Field(..., description="Логин")
    token: Optional[str] = Field(..., description="Токен для сброса пароля")
    old_password: Optional[str] = Field(None, serialization_alias='oldPassword')
    new_password: Optional[str] = Field(None, serialization_alias='newPassword')