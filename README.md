# Cloud Service Access Management System

A FastAPI-based backend for managing user access to cloud services, with role-based permissions, usage tracking, and JWT authentication.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Getting Started](#getting-started)  
   1. [Prerequisites](#prerequisites)  
   2. [Installation](#installation)  
   3. [Running the Server](#running-the-server)  
3. [Project Structure](#project-structure)  
4. [Features](#features)
   1. [User Management](#user-management)
   2. [JWT Authentication](#jwt-authentication)
   3. [Cloud Service CRUD](#cloud-service-crud)
   4. [Access Control](#access-control)
   5. [Service Invocation](#service-invocation)
   6. [Usage Tracking](#usage-tracking)
   7. [Rate Limiting](#rate-limiting)
   8. [Database](#database)
   9. [Linting & CI](#linting--ci)
   10. [Plans & Permissions](#plans--permissions)
5. [API Documentation](#api-documentation)

---

## Introduction

This project provides a backend system that dynamically manages access to multiple cloud-style APIs based on user subscriptions and permissions. It offers secure user sign-up/login with password hashing and JWTs, full CRUD for services and permissions, fine-grained access control, and detailed usage logging to support rate-limiting policies.

---

## Getting Started

### Prerequisites

- Python 3.12+  
- Git  

### Installation

1. Clone the repo:  
```bash
git clone https://github.com/JulioAnzaldo/CPSC-446-Final-Project
cd cloud-access-management
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the server
```bash
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000/docs.

## Project structure
```
project/
├── app/
│   ├── main.py             # FastAPI app setup & router includes
│   ├── db.py               # SQLAlchemy engine & session
│   ├── models.py           # ORM models (User, Service, AccessControl, UsageRecord)
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── routers/
│   │   ├── users.py        # User CRUD & signup
│   │   ├── auth.py         # JWT login & current-user dependency
│   │   ├── services.py     # Service CRUD & invocation endpoint
│   │   ├── access_controls.py  # Assign/revoke permissions
│   │   └── usage.py        # Usage statistics endpoints
│   └── utils/
│       ├── security.py     # Password hashing & JWT helpers
│       └── access.py       # Access-control verification dependencies
├── scripts/                # CLI scripts for admin tasks (e.g. create/reset users)  
├── .gitignore  
├── .pre-commit-config.yaml  
├── pyproject.toml          # Black & isort config  
├── requirements.txt  
└── README.md
```

## Features

## User Management
- Create, list, and retrieve users
- Secure password hashing using bcrypt via Passlib

## JWT Authentication
- OAuth2 password flow `(/auth/token)`
- `Bearer` token issuance and validation
- **GET** `/users/me` to fetch current user profile

## Cloud Service CRUD
- **POST** `/services/` – add new services
- **GET** `/services/` – list all services
- **GET** `/services/{id}` – retrieve a service
- **PUT** `/services/{id}` – update service details
- **DELETE** /`services/{id}` – remove a service

## Access Control
- Access Control
- **POST** `/access-controls/` – assign a permission to a user for a service
- **GET** `/access-controls/` – list all assignments
- **GET** `/access-controls/{id}` – retrieve an assignment
- **DELETE** `/access-controls/{id}` – revoke a permission

## Service Invocation
- **GET** `/services/{id}/call`
- Protected by “read” permission
- Returns service metadata

## Usage Tracking
- Logs each successful `/services/{id}/call` with timestamp
- **GET** `/usage/me` – retrieve personal usage history

## Rate Limiting
- Rate Limiting
- Middleware/dependency-ready hooks to enforce per-user or per-plan limits
- Configurable windows (e.g., per minute, per month)

## Database
- Uses SQLite for local development
- No database migration tools (e.g. Alembic) are used
- Tables are auto-created from SQLAlchemy models

## Linting & CI
- Black and isort for code formatting
- Flake8 for linting
- pre-commit hooks to enforce style rules automatically

## Plans & Permissions
- **POST** `/permissions/` – create new permission types
- **GET** `/permissions/` – list all permissions
- **POST** `/plans/` – create subscription plans
- **PUT** `/plans/{id}` – update a plan
- **GET** `/plans/` – list plans
- **DELETE** `/plans/{id}` – delete a plan
- **PUT** `/users/{id}/plan` – assign a user to a plan

## API Documentation
Visit interactive docs at:
```
http://127.0.0.1:8000/docs
```

You can explore and test all endpoints directly from your browser.
