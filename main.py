from __future__ import annotations

import os
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException, status
import mysql.connector
from pydantic import BaseModel, Field

from models.transaction import Transaction
from models.new_transaction_request import NewTransactionRequest

port = int(os.environ.get("FASTAPIPORT", 8000))


# -----------------------------------------------------------------------------
# FastAPI App Definition
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Transaction API",
    description="Am API to manage transactions.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# Connect to db
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Transaction API",
    description="Am API to manage transactions.",
    version="1.0.0",
)
db_config = {
    "host": "136.113.127.151",          
    "user": "microservice_3",             
    "password": "arknights123",    
    "database": "neighborhood_db"          
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    print("✅ Database connected successfully")
except Exception as e:
    print("❌ Database connection failed:", e)


def row_to_transaction(row: dict) -> Transaction:
    return Transaction(
        transactionId=row["transactionId"],
        itemId=row["itemId"],
        initiatorUserId=str(row["initiatorUserId"]),
        receiverUserId=str(row["receiverUserId"]),
        status=row["status"],
        createdAt=row["createdAt"],
        updatedAt=row["updatedAt"],
    )


class UpdateStatusRequest(BaseModel):
    status: Literal["completed", "canceled"] = Field(..., description="New status")


# -----------------------------------------------------------------------------
# Root Endpoint
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Transaction API. See /docs for details."}


# -----------------------------------------------------------------------------
# Transaction Endpoints
# -----------------------------------------------------------------------------
@app.post("/transactions/transaction", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: NewTransactionRequest):
    try:
        cursor.execute(
            "INSERT INTO transactions (itemId, initiatorUserId, receiverUserId, status) VALUES (%s, %s, %s, %s)",
            (transaction.itemId, transaction.initiatorUserId, transaction.receiverUserId, transaction.status),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM transactions WHERE transactionId = %s", (new_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to load created transaction")
        return row_to_transaction(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/transactions/{transactionId}", response_model=Transaction)
def get_transaction(transactionId: int):
    try:
        cursor.execute("SELECT * FROM transactions WHERE transactionId = %s", (transactionId,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return row_to_transaction(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/transactions", response_model=list[Transaction])
def list_transactions(
    status_param: Optional[Literal["pending", "completed", "canceled"]] = None,
    initiatorUserId: Optional[str] = None,
    receiverUserId: Optional[str] = None,
    itemId: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
):
    try:
        conditions = []
        params: list = []
        if status_param is not None:
            conditions.append("status = %s")
            params.append(status_param)
        if initiatorUserId is not None:
            conditions.append("initiatorUserId = %s")
            params.append(initiatorUserId)
        if receiverUserId is not None:
            conditions.append("receiverUserId = %s")
            params.append(receiverUserId)
        if itemId is not None:
            conditions.append("itemId = %s")
            params.append(itemId)

        where_clause = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"SELECT * FROM transactions{where_clause} ORDER BY createdAt DESC LIMIT %s OFFSET %s"
        params.append(limit)
        params.append(offset)
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        return [row_to_transaction(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/transactions/{transactionId}", response_model=Transaction)
def update_transaction(transactionId: int, payload: UpdateStatusRequest):
    try:
        cursor.execute("SELECT * FROM transactions WHERE transactionId = %s", (transactionId,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        cursor.execute("UPDATE transactions SET status = %s WHERE transactionId = %s", (payload.status, transactionId))
        conn.commit()
        cursor.execute("SELECT * FROM transactions WHERE transactionId = %s", (transactionId,))
        updated = cursor.fetchone()
        return row_to_transaction(updated)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/transactions/{transactionId}", response_model=Transaction)
def delete_transaction(transactionId: int):
    try:
        cursor.execute("SELECT * FROM transactions WHERE transactionId = %s", (transactionId,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        cursor.execute("DELETE FROM transactions WHERE transactionId = %s", (transactionId,))
        conn.commit()
        return row_to_transaction(existing)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
