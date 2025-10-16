
# Neighbourhood Exchange - Transaction 

## Overview

The **Transaction Service** is a core component of the **Neighbourhood Exchange** platform. It manages user-to-user item exchange transactions, allowing users to initiate, update, retrieve, and delete transaction records between participants.

This service defines the data model (`Transaction`) and provides RESTful API endpoints for performing **CRUD (Create, Read, Update, Delete)** operations on transactions.

---

## Data Model

### `Transaction`

The `Transaction` class defines the schema for transaction objects handled by this service.

| Field             | Type       | Description                                                                             | Example                 |
| ----------------- | ---------- | --------------------------------------------------------------------------------------- | ----------------------- |
| `transactionId`   | `int`      | Unique identifier for the transaction.                                                  | `5`                     |
| `itemId`          | `int`      | The ID of the item being requested.                                                     | `8`                     |
| `initiatorUserId` | `str`      | ID of the user who initiated the transaction.                                           | `"4"`                   |
| `receiverUserId`  | `str`      | ID of the user who owns the requested item.                                             | `"6"`                   |
| `status`          | `str`      | Current status of the transaction. Possible values: `pending`, `completed`, `canceled`. | `"pending"`             |
| `createdAt`       | `datetime` | Timestamp when the transaction was created.                                             | `"2023-01-01T00:00:00"` |
| `updatedAt`       | `datetime` | Timestamp when the transaction was last updated.                                        | `"2023-01-01T00:00:00"` |

This model is implemented using **Pydantic**, providing strong typing, validation, and automatic schema generation for OpenAPI documentation.

---

## API Endpoints

### 1. Create Transaction (Initiate a Transaction Request)

**Endpoint:** `POST /transactions/transaction`
**Purpose:** To create a new transaction request between two users for a specific item.

**Requirements:**
Essential information must be provided, including:

* `itemId` – ID of the item being requested.
* `initiatorUserId` – ID of the user initiating the transaction.
* `receiverUserId` – ID of the user who owns the requested item.
* `status` – Current status of the transaction (`pending`, `completed`, or `canceled`).

**System Action:**
The system automatically assigns a unique `transactionId` and records the `createdAt` timestamp.

---

### 2. Get Transaction (Retrieve Transaction Details)

**Endpoint:** `GET /transactions/{transactionId}`

**Purpose:** To retrieve details of a specific transaction by its unique ID.

**Requirements:**

* `transactionId` (path parameter) must be provided.

**System Action:**
The system fetches and returns the transaction record that matches the given `transactionId`.

**Possible Errors:**

* `404` – Transaction not found.

---

### 3. Update Transaction (Modify Transaction Details or Status)

**Endpoint:** `PUT /transactions/{transactionId}`
**Purpose:** To update an existing transaction, such as changing its status or modifying related details.

**Requirements:**

* `transactionId` (path parameter) must be provided.
* Updated transaction data in the request body (e.g., new `status`).

**System Action:**
The system updates the specified transaction and records the `updatedAt` timestamp.

**Possible Errors:**

* `400` – Invalid input.
* `404` – Transaction not found.

---

### 4. Delete Transaction (Remove a Transaction Record)

**Endpoint:** `DELETE /transactions/{transactionId}`
**Purpose:** To delete a transaction record from the system.

**Requirements:**

* `transactionId` (path parameter) must be provided.

**System Action:**
The system permanently removes the transaction from the database.

**Possible Errors:**

* `404` – Transaction not found.

---


## Implementation Notes

* These endpoints are **not yet implemented** — they serve as placeholders for the backend logic.
* Once implemented, they will likely interact with a database to manage transaction records.
* Timestamps (`createdAt`, `updatedAt`) should be automatically managed by the backend.
* Recommended frameworks: **FastAPI** or **Flask** for Python-based implementations.

---


# Sprint 1 - Microservice 3

[Swagger Editor](https://editor.swagger.io/)

Transactions

## Requirement

Use Swagger to do API 1st definition of the microservice’s API. You do not need to generate code from the API definition

You should have paths for each “resource” implementing GET, PUT, POST, DELETE. The methods can simply return NOT IMPLEMENTED.
