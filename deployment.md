# 🍚 Biryani Direct — Deployment & Local Setup Guide

## 1. Demo Login Credentials (For Reviewer Testing)

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Superadmin / CMS** | admin | admin1234 | Full Django Admin Access |
| **Customer User** | customer1 | test1234 | Outlet Selection, Menu, Cart, Checkout, Order Tracking |
| **Kitchen Staff** | kitchen1 | test1234 | Dark-Mode Kitchen Display System (KDS) & Status Updates |

---

## 2. Step-by-Step Local Setup

### Prerequisites
- Python 3.11+ installed
- Git installed

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd biryani-direct

2. **Create & activate virtual environment:**

python -m venv venv
# On Windows:
.\venv\Scripts\activate

3. **Install dependencies:**
pip install django

4. **Apply database migrations:**
python manage.py migrate

5. **Start the local development server:**
python manage.py runserver


6. **Access the application:**
Open browser at http://127.0.0.1:8000/