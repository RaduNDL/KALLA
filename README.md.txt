# KÄLLA - Artisan Coffee Shop Platform

KÄLLA is a modern, full-stack web application designed for boutique coffee shops. It allows users to browse menus, customize orders, and manage their accounts, while providing staff with a powerful dashboard for inventory and order management.

## Tech Stack

- **Frontend**: Vue.js 3, Pinia, Vue Router, Tailwind CSS.
- **Backend**: FastAPI (Python), PostgreSQL, Bcrypt, PyJWT.

## Key Features

- **Customer Portal**:
    - Product browsing with category filtering.
    - Advanced product customization (sugar, milk, flavors).
    - Shopping cart & secure checkout process.
    - User profile & order history.
- **Employee Portal**:
    - Full Product CRUD (Add, Edit, Delete).
    - Real-time Order Status Management.
    - Role-based Access Control.

## Getting Started

### 1. Database Setup
Ensure PostgreSQL is running with the `coffeeshop` database and your credentials in `main.py`.

### 2. Backend (API)
Navigate to `E:\PersonalProjects\API` and run:
```bash
python setup_employee.py
python main.py