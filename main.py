from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, status

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
# Root Endpoint
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Transaction API. See /docs for details."}


# -----------------------------------------------------------------------------
# Transaction Endpoints
# -----------------------------------------------------------------------------
@app.post("/transactions/transaction", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: Transaction):
    return True

@app.get("/transactions/{transactionId}", response_model=Transaction)
def get_transaction(transactionId: int):
    return

@app.put("/transactions/{transactionId}", response_model=Transaction)
def update_transaction(transactionId: int, updated_transaction: Transaction):
    return 

@app.delete("/transactions/{transactionId}", response_model=Transaction)
def delete_transaction(transactionId: int):
    return

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
