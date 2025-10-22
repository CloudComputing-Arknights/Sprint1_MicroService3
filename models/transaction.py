from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transactionId: int = Field(
        ..., 
        description="The unique identifier for the transaction.", 
        json_schema_extra={"example": 5},
    )
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
        ..., 
        description="The current status of the transaction.", 
        json_schema_extra={"example": "pending"},
    )
    createdAt: datetime = Field(
        ..., 
        description="The timestamp when the transaction was created.", 
        json_schema_extra={"example": "2023-01-01T00:00:00"},
    )
    updatedAt: datetime = Field(
        ..., 
        description="The timestamp when the transaction was last updated.", 
        json_schema_extra={"example": "2023-01-01T00:00:00"},
    )