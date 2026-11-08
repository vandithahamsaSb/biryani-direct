# 🍛 Biryani Direct

> A full-stack Django food ordering platform and real-time Kitchen Display System (KDS) powered by AI, designed for a multi-outlet cloud kitchen network in Hyderabad.

---

## ✨ Key Features

### 🛍️ Customer Experience
* **Seamless Ordering:** Browse authentic Hyderabadi Dum Biryani, customize items, add to cart, and checkout seamlessly.
* **Promo Engine:** Integrated coupon system (e.g., `BIRYANI10` for discounts).
* **AI Reorder Recommendations:** Smartly analyzes user history to suggest favorite dishes.
* **Modern UI/UX:** Responsive Bootstrap 5 interface themed in Saffron Orange (`#E65100`) with dynamic toast notifications.

### 👨‍🍳 Kitchen & Operations
* **Live KDS (Kitchen Display System):** Specialized dark-mode dashboard for kitchen staff to track and update order statuses in real-time.
* **AI Prep Time Predictor:** Dynamically estimates kitchen preparation times based on active order volume and items.
* **Multi-Outlet Support:** Configured to manage 14 standard outlets and 3 cloud kitchens across Hyderabad.

---

## 📸 System Screenshots

*(Tip: Drag & drop your project screenshots directly into this section when editing on GitHub)*

---

## 🛠️ Tech Stack

* **Backend:** Python 3.11, Django 5.x
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **AI Engine:** Custom algorithmic prediction engine (`core/ai.py`)

---

## 🚀 Local Setup & Installation

Follow these steps to run the application on your local system:

```bash
# 1. Clone the repository
git clone https://github.com/vandithahamsaSb/biryani-direct.git
cd biryani-direct

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install django

# 4. Migrate database and seed test data
python manage.py migrate
python seed_data.py

# 5. Start the development server
python manage.py runserver      
