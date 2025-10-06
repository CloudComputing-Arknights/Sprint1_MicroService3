from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NewTransactionRequest(BaseModel):
    itemId: Optional[int] = Field(
        ...,
        description="The ID of the item being requested by the initiator.",
        json_schema_extra={"example": 8},
    )
    initiatorUserId: Optional[str] = Field(
        ...,
        description="The ID of the user who started the transaction.",
        json_schema_extra={"example": 4},
    )
    receiverUserId: Optional[str] = Field(
        ...,
        description="The ID of the user who owns the requested item.",
        json_schema_extra={"example": 6},
    )
    status: Optional[str] = Field(
        ...,
        description="The current status of the transaction.",
        json_schema_extra={"example": "pending"},
    )