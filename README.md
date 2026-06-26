# 🛒 E-Commerce Backend API

A full-featured **RESTful e-commerce backend** built with **FastAPI** and **PostgreSQL**. This API provides complete backend functionality for an e-commerce platform including user management, product catalog, order processing, wallet system, role-based access control, and JWT authentication.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
  - [Root](#root)
  - [Authentication](#authentication)
  - [Users](#users)
  - [Products](#products)
  - [Orders](#orders)
- [Role-Based Access Control (RBAC)](#-role-based-access-control-rbac)
- [Authentication & Security](#-authentication--security)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
  - [Running the Server](#running-the-server)
- [Database Migrations](#-database-migrations)
- [Configuration](#-configuration)
- [License](#-license)

---

## ✨ Features

- **User Registration & Authentication** — Secure sign-up and login with JWT (JSON Web Token) based authentication.
- **Password Hashing** — Passwords are hashed using the **Argon2** algorithm (winner of the Password Hashing Competition) via Passlib.
- **Role-Based Access Control (RBAC)** — Three-tier role system: `customer`, `admin`, and `superadmin` with granular permission enforcement.
- **Product Management** — Full CRUD operations for products with support for filtering by type, warehouse location, and discount status.
- **Discount System** — Admin/superadmin can apply and manage discount percentages on individual products.
- **Digital Wallet** — Users have an in-app wallet to add funds and make purchases.
- **Order Lifecycle Management** — Complete order flow including placing, canceling, and shipping orders with automatic inventory and wallet adjustments.
- **Inventory Tracking** — Real-time inventory updates when orders are placed or canceled.
- **User Promotion** — Superadmins can promote regular users to admin role.
- **Query Filtering** — Products can be filtered by product type, warehouse pincode, and discount status via query parameters.
- **Database Migrations** — Schema versioning and migration management using Alembic.
- **Input Validation** — Request/response validation using Pydantic v2 schemas with email validation.
- **Auto-generated API Docs** — Interactive Swagger UI (`/docs`) and ReDoc (`/redoc`) documentation powered by FastAPI.

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | High-performance async web framework |
| [PostgreSQL](https://www.postgresql.org/) | Relational database |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM (Object-Relational Mapper) |
| [Alembic](https://alembic.sqlalchemy.org/) | Database migrations |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation & serialization |
| [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Environment variable management |
| [python-jose](https://python-jose.readthedocs.io/) | JWT token creation & verification |
| [Passlib](https://passlib.readthedocs.io/) + [Argon2](https://argon2-cffi.readthedocs.io/) | Password hashing |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Psycopg2](https://www.psycopg.org/) | PostgreSQL adapter for Python |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` file loading |

---

## 📁 Project Structure

```
e_commerce/
├── alembic/                        # Alembic migration configuration
│   ├── env.py                      # Migration environment setup (reads DB URL from settings)
│   ├── script.py.mako              # Migration script template
│   ├── README                      # Alembic readme
│   └── versions/                   # Auto-generated migration scripts
│       ├── e1ff59ebc4ba_...py      # Initial table creation
│       ├── f4c4048f83fe_...py      # Product table columns (v1)
│       ├── 48d1db7c86e2_...py      # Separated user & product tables
│       ├── f27a4628d4f1_...py      # Added user created_at timestamp
│       ├── ca91e46dd5de_...py      # Added role column to user table
│       ├── dc8eb76e2d21_...py      # Created order table
│       ├── e08bb30a9b16_...py      # Added product_name to order table
│       └── 9a57e959269b_...py      # Added order_price to order table
│
├── app/                            # Main application package
│   ├── __init__.py                 # Package initializer
│   ├── main.py                     # FastAPI app entry point & router registration
│   ├── config.py                   # Settings management (loads from .env)
│   ├── database.py                 # SQLAlchemy engine, session, and Base setup
│   ├── models.py                   # SQLAlchemy ORM models (Product, User, Order)
│   ├── schemas.py                  # Pydantic request/response schemas
│   ├── utils.py                    # Password hashing & verification utilities
│   ├── OAuth2.py                   # JWT token creation, verification & user extraction
│   └── routers/                    # API route handlers
│       ├── auth.py                 # Login endpoint
│       ├── user.py                 # User CRUD, wallet, & promotion endpoints
│       ├── product.py              # Product CRUD, filtering, & discount endpoints
│       └── order.py                # Order placement, cancellation, shipping & retrieval
│
├── .env                            # Environment variables (not committed to git)
├── .gitignore                      # Git ignore rules
├── alembic.ini                     # Alembic configuration file
├── requirements.txt                # Python dependencies
└── venv/                           # Python virtual environment (not committed to git)
```

---

## 🗄 Database Schema

The application uses **three database tables** managed via SQLAlchemy ORM:

### `product` Table

| Column | Type | Constraints | Default | Description |
|---|---|---|---|---|
| `id` | Integer | Primary Key, NOT NULL | Auto-increment | Unique product identifier |
| `product_name` | String | NOT NULL | — | Name of the product |
| `inventory` | Integer | NOT NULL | — | Available stock count |
| `created_at` | Timestamp (TZ) | NOT NULL | `now()` | Product creation timestamp |
| `product_type` | String | NOT NULL | — | Category/type of product |
| `discount_status` | Boolean | NOT NULL | `false` | Whether discount is active |
| `discount_percent` | Integer | NOT NULL | `0` | Discount percentage (0–100) |
| `warehouse_pincode` | Integer | NOT NULL | — | Pincode of the warehouse location |
| `price` | Integer | NOT NULL | `100` | Price of the product |

### `user` Table

| Column | Type | Constraints | Default | Description |
|---|---|---|---|---|
| `id` | Integer | Primary Key, NOT NULL | Auto-increment | Unique user identifier |
| `email` | String | NOT NULL, UNIQUE | — | User email address |
| `password` | String | NOT NULL | — | Argon2-hashed password |
| `user_pincode` | Integer | NOT NULL | — | User's location pincode |
| `created_at` | Timestamp (TZ) | NOT NULL | `now()` | Account creation timestamp |
| `wallet` | Integer | NOT NULL | `0` | Wallet balance |
| `completed_order` | Integer | NOT NULL | `0` | Count of completed orders |
| `pending_order` | Integer | NOT NULL | `0` | Count of pending orders |
| `failed_order` | Integer | NOT NULL | `0` | Count of canceled/failed orders |
| `role` | String | NOT NULL | `'customer'` | User role (`customer`, `admin`, `superadmin`) |

### `order` Table

| Column | Type | Constraints | Default | Description |
|---|---|---|---|---|
| `order_id` | Integer | Primary Key, NOT NULL | Auto-increment | Unique order identifier |
| `user_id` | Integer | FK → `user.id`, ON DELETE CASCADE, NOT NULL | — | ID of the user who placed the order |
| `product_id` | Integer | FK → `product.id`, ON DELETE CASCADE, NOT NULL | — | ID of the ordered product |
| `quantity` | Integer | NOT NULL | — | Quantity ordered |
| `created_at` | Timestamp (TZ) | NOT NULL | `now()` | Order creation timestamp |
| `order_status` | String | NOT NULL | — | Status: `placed`, `shipped`, or `canceled` |
| `product_name` | String | NOT NULL | — | Name of the product (denormalized) |
| `order_price` | Integer | NOT NULL | — | Total price for the order |

### Entity Relationship

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│  User    │        │  Order   │        │ Product  │
├──────────┤        ├──────────┤        ├──────────┤
│ id (PK)  │◄───────│ user_id  │        │ id (PK)  │
│ email    │        │ order_id │        │ name     │
│ password │        │product_id│───────►│ price    │
│ wallet   │        │ quantity │        │ inventory│
│ role     │        │ status   │        │ discount │
└──────────┘        └──────────┘        └──────────┘
```

---

## 📡 API Endpoints

### Root

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | Welcome message | No |

---

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/login/` | User login (returns JWT token) | No |

**Request Body** (`OAuth2PasswordRequestForm`):
- `username` — User's email address
- `password` — User's password

**Response** (`Token`):
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

---

### Users

| Method | Endpoint | Description | Auth Required | Role Required |
|---|---|---|---|---|
| `POST` | `/users/` | Register a new user | No | — |
| `GET` | `/users/` | List all users | Yes | `admin` / `superadmin` |
| `POST` | `/users/wallet` | Add money to wallet | Yes | Any |
| `GET` | `/users/wallet` | Check wallet balance | Yes | Any |
| `POST` | `/users/promote` | Promote a user to admin | Yes | `superadmin` |

**Create User Request** (`User`):
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "user_pincode": 110001
}
```

**Create User Response** (`UserResponse`):
```json
{
  "email": "user@example.com",
  "user_pincode": 110001,
  "id": 1
}
```

**Add Money to Wallet** (`Wallet`):
```json
{
  "wallet": 5000
}
```

**Promote User** (`UpgradeUser`):
```json
{
  "username": "user@example.com"
}
```

---

### Products

| Method | Endpoint | Description | Auth Required | Role Required |
|---|---|---|---|---|
| `POST` | `/products/` | Create a new product | Yes | `superadmin` |
| `GET` | `/products/` | List all products (with optional filters) | Yes | Any |
| `GET` | `/products/{id}` | Get a specific product by ID | Yes | Any |
| `PUT` | `/products/{id}` | Update a product | Yes | `admin` / `superadmin` |
| `DELETE` | `/products/{id}` | Delete a product | Yes | `superadmin` |
| `PUT` | `/products/discount/{id}` | Update discount on a product | Yes | `admin` / `superadmin` |

**Query Parameters for `GET /products/`**:

| Parameter | Type | Description |
|---|---|---|
| `ProductType` | string | Filter by product type/category |
| `WarehousePin` | integer | Filter by warehouse pincode |
| `DiscountStatus` | boolean | Filter by discount availability |

**Create/Update Product** (`Product`):
```json
{
  "product_name": "Wireless Headphones",
  "inventory": 150,
  "product_type": "electronics",
  "warehouse_pincode": 400001,
  "discount_status": false,
  "discount_percent": 0
}
```

**Update Discount** (`Discount`):
```json
{
  "discount_status": true,
  "discount_percent": 20
}
```

---

### Orders

| Method | Endpoint | Description | Auth Required | Role Required |
|---|---|---|---|---|
| `POST` | `/orders/` | Place a new order | Yes | Any |
| `GET` | `/orders/` | Get all orders for current user | Yes | Any |
| `POST` | `/orders/cancel` | Cancel an order | Yes | Any (own orders) |
| `POST` | `/orders/ship` | Mark an order as shipped | Yes | `admin` / `superadmin` |

**Place Order** (`PlaceOrder`):
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Cancel / Ship Order** (`CancelProduct`):
```json
{
  "order_id": 1
}
```

#### Order Lifecycle

```
 ┌─────────┐    User Action    ┌───────────┐   Admin Action   ┌──────────┐
 │  PLACED  │ ───────────────► │  CANCELED  │                  │          │
 │         │                   └───────────┘                  │          │
 │         │ ─────────────────────────────────────────────►   │ SHIPPED  │
 └─────────┘                                                  └──────────┘
```

**Order placement logic:**
1. Validates the product exists
2. Calculates total price (`product.price × quantity`)
3. Checks if the user's wallet has sufficient balance
4. Deducts the amount from the user's wallet
5. Decrements the product inventory
6. Increments the user's `pending_order` count
7. Creates the order record with status `placed`

**Order cancellation logic:**
1. Validates the order exists and belongs to the current user
2. Checks the order isn't already `canceled` or `shipped`
3. Restores the amount to the user's wallet
4. Restores the product inventory
5. Updates order counters (`pending_order` ↓, `failed_order` ↑)
6. Sets order status to `canceled`

**Order shipping logic (admin/superadmin only):**
1. Validates the order exists
2. Checks the order isn't already `shipped` or `canceled`
3. Updates order counters (`pending_order` ↓, `completed_order` ↑)
4. Sets order status to `shipped`

---

## 🔐 Role-Based Access Control (RBAC)

The system implements a **three-tier role hierarchy**:

| Role | Description | Permissions |
|---|---|---|
| `customer` | Default role for new users | Browse products, manage wallet, place/cancel own orders, view own orders |
| `admin` | Promoted by superadmin | All customer permissions + update products, manage discounts, ship orders, view all users |
| `superadmin` | Highest privilege | All admin permissions + create/delete products, promote users to admin |

### Permission Matrix

| Action | Customer | Admin | Superadmin |
|---|---|---|---|
| Register / Login | ✅ | ✅ | ✅ |
| Browse Products | ✅ | ✅ | ✅ |
| Manage Own Wallet | ✅ | ✅ | ✅ |
| Place / Cancel Orders | ✅ | ✅ | ✅ |
| View Own Orders | ✅ | ✅ | ✅ |
| Update Products | ❌ | ✅ | ✅ |
| Manage Discounts | ❌ | ✅ | ✅ |
| Ship Orders | ❌ | ✅ | ✅ |
| View All Users | ❌ | ✅ | ✅ |
| Create Products | ❌ | ❌ | ✅ |
| Delete Products | ❌ | ❌ | ✅ |
| Promote Users | ❌ | ❌ | ✅ |

---

## 🔒 Authentication & Security

- **Authentication Method**: OAuth2 with Password (Bearer Token) flow
- **Token Type**: JWT (JSON Web Token)
- **Signing Algorithm**: HS256
- **Token Expiry**: 60 minutes (configurable via `.env`)
- **Password Hashing**: Argon2 via Passlib
- **Token Endpoint**: `POST /login/`

### Authentication Flow

```
1. User registers  →  POST /users/         →  Password hashed with Argon2, stored in DB
2. User logs in    →  POST /login/          →  Credentials verified, JWT token returned
3. User makes request  →  Authorization: Bearer <token>  →  Token decoded, user extracted
```

All protected endpoints use FastAPI's `Depends(OAuth2.get_current_user)` dependency injection to automatically extract and validate the current user from the JWT token.

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.10+
- **PostgreSQL** 12+
- **pip** (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd e_commerce
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=ecom
DATABASE_USERNAME=postgres
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

| Variable | Description | Example |
|---|---|---|
| `DATABASE_HOSTNAME` | PostgreSQL host | `localhost` |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `DATABASE_USERNAME` | Database username | `postgres` |
| `DATABASE_PASSWORD` | Database password | `your_password` |
| `DATABASE_NAME` | Database name | `ecom` |
| `SECRET_KEY` | JWT signing secret key | A long random hex string |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes | `60` |

> ⚠️ **Important**: Generate a strong, random `SECRET_KEY` for production. You can use:
> ```bash
> openssl rand -hex 32
> ```

### Database Setup

1. **Create the PostgreSQL database**:
   ```sql
   CREATE DATABASE ecom;
   ```

2. **Run Alembic migrations** to set up the schema:
   ```bash
   alembic upgrade head
   ```

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **`http://127.0.0.1:8000`**

#### Interactive API Documentation

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔄 Database Migrations

This project uses **Alembic** for database migration management. The migration history tracks the evolution of the database schema:

| Migration | Description |
|---|---|
| `e1ff59ebc4ba` | Initial table creation |
| `f4c4048f83fe` | Added product columns (v1 of product schema) |
| `48d1db7c86e2` | Separated user & product into distinct tables |
| `f27a4628d4f1` | Added `created_at` timestamp to user table |
| `ca91e46dd5de` | Added `role` column to user table |
| `dc8eb76e2d21` | Created order table with foreign keys |
| `e08bb30a9b16` | Added `product_name` to order table |
| `9a57e959269b` | Added `order_price` to order table |

### Common Migration Commands

```bash
# Apply all pending migrations
alembic upgrade head

# Generate a new migration after model changes
alembic revision --autogenerate -m "description of change"

# Downgrade by one revision
alembic downgrade -1

# View current migration state
alembic current

# View migration history
alembic history
```

---

## ⚙ Configuration

All configuration is managed through the `Settings` class in `app/config.py` using **Pydantic Settings**. Environment variables are loaded from the `.env` file automatically.

```python
class Settings(BaseSettings):
    database_username: str
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
```

The database connection URL is constructed dynamically:
```
postgresql://{username}:{password}@{hostname}:{port}/{database_name}
```

---

## 📄 License

This project is open source and available for educational and personal use.
