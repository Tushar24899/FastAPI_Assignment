# FastAPI Address Book API

## Overview

This project is a **FastAPI-based Address Book service** that allows users to manage addresses and find nearby locations based on geographic coordinates.

The application is built using **FastAPI, SQLAlchemy (Async), and SQLite**, following a clean architecture with **routers, services, and repositories**.

---

## Features

- Create a new address
- Retrieve all stored addresses
- Update an existing address
- Delete an address
- Find addresses within a given distance
- Async database operations
- Structured logging
- Dependency Injection
- Auto-generated API documentation (Swagger)

---

## Tech Stack

- **FastAPI** – API framework
- **SQLAlchemy (Async)** – ORM for database operations
- **SQLite** – Lightweight database
- **Poetry** – Dependency management
- **Geopy** – Distance calculation between coordinates

---

## Project Structure

```
src/
│
├── address_book_api/
│   ├── api/
│   │   ├── api_router.py
│   │   └── routes/
│   │       └── address_book.py
│   │
│   ├── db/
│   │   ├── db.py
│   │   └── repository/
│   │       └── address_repository.py
│   │
│   ├── models/
│   │   └── address.py
│   │
│   ├── schema/
│   │   └── address.py
│   │
│   └── service/
│       └── address.py
│
└── main.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/FastAPI_Assignment.git
cd FastAPI_Assignment
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Activate virtual environment

```bash
poetry shell
```

### 4. Run the application

```bash
poetry run start-address_book
```

The API will start at:

```
http://localhost:8000
```

---

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## API Endpoints

### Create Address

```
POST /addresses
```

Example Request

```json
{
  "name": "Home",
  "street": "MG Road",
  "city": "Bangalore",
  "latitude": 12.9716,
  "longitude": 77.5946
}
```

---

### Get All Addresses

```
GET /addresses
```

---

### Update Address

```
PUT /addresses/{address_id}
```

---

### Delete Address

```
DELETE /addresses/{address_id}
```

---

### Find Nearby Addresses

```
GET /addresses/nearby
```

Query Parameters

```
latitude
longitude
distance_km
```

Example

```
/addresses/nearby?latitude=12.9716&longitude=77.5946&distance_km=5
```

---

## Logging

The application uses structured logging to track API requests and database operations.

---

## Author

Tushar Dhiman
