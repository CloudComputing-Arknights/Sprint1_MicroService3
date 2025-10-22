from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class NewTransactionRequest(BaseModel):
    itemId: int = Field(
        ..., 
        description="The ID of the item being requested by the initiator.", 
        json_schema_extra={"example": 8},
    )
    initiatorUserId: str = Field(
        ..., 
        description="The ID of the user who started the transaction.", 
        json_schema_extra={"example": "4"},
    )
    receiverUserId: str = Field(
        ..., 
        description="The ID of the user who owns the requested item.", 
        json_schema_extra={"example": "6"},
    )
    status: Literal["pending", "completed", "canceled"] = Field(
        default="pending", 
        description="The current status of the transaction.", 
        json_schema_extra={"example": "pending"},
    )