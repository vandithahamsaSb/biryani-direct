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
<img width="1350" height="633" alt="image" src="https://github.com/user-attachments/assets/eef040b1-575a-4f34-b7aa-9810f1219d0b" />
<img width="1338" height="555" alt="image" src="https://github.com/user-attachments/assets/2b6eaac3-9d1d-4e77-b9c7-3b21a6830b2e" />
<img width="1291" height="605" alt="image" src="https://github.com/user-attachments/assets/dab9df5f-e74c-42c1-8c2b-b45a20701b44" />
<img width="1360" height="635" alt="image" src="https://github.com/user-attachments/assets/c46d977f-7149-4aec-aa62-046d3391f7ee" />
<img width="1187" height="633" alt="image" src="https://github.com/user-attachments/assets/c53c383c-bea7-4039-90f4-99920b7a892e" />
<img width="1237" height="618" alt="image" src="https://github.com/user-attachments/assets/08aa593e-cfa8-461f-a780-219ee148c722" />
<img width="698" height="262" alt="image" src="https://github.com/user-attachments/assets/b1ac1afd-ed76-4485-afc2-63d2f121d8c8" />








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
