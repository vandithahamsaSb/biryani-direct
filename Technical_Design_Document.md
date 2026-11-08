# 🍚 Biryani Direct — Technical Design Document (TDD)

**GitHub Repository URL:** `https://github.com/YOUR_GITHUB_USERNAME/biryani-direct`  
*(Note: Replace with your public GitHub repository link after pushing)*

---

## 1. Executive Summary & Core Build
**Biryani Direct** is a full-stack food ordering platform and Kitchen Display System (KDS) built for a 14-outlet and 3-cloud-kitchen Hyderabadi biryani chain. The platform eliminates 27% aggregator commissions by enabling direct customer ordering with transparent 5% GST pricing and live AI prep-time estimates.

---

## 2. System Architecture & Tech Stack Choice
- **Backend Framework:** Python 3.11 with Django 5.x — chosen for built-in ORM, robust session authentication, role-based access control, and rapid administrative tooling.
- **Database:** SQLite3 for lightweight development and seamless demonstration portability.
- **Frontend & UX:** HTML5, Bootstrap 5, custom soft light saffron theme (`#FFF0E5`) with orange accent buttons (`#E65100`), responsive on mobile and desktop devices.
- **Real-Time KDS:** Low-overhead AJAX Polling (`/kitchen/api/`) updating every 5 seconds without requiring full page refreshes.

---

## 3. Core Data Model & Entities
- **Outlet:** Stores location name, type (Dine-in / Cloud Kitchen), address, and `minimum_prep_time` across 14 outlets + 3 cloud kitchens in Hyderabad.
- **MenuItem:** Stores dish details, price, `prep_minutes`, veg/non-veg status, and spice levels.
- **Order:** Tracks unique order codes (e.g. `WEB-778120`), assigned outlet, customer, timestamp, total price, and live status (`RECEIVED`, `PREPARING`, `READY`, `DELIVERED`).
- **OrderItem:** Maps menu items and quantities to specific orders.

---

## 4. AI Engine & Smart Features (`core/ai.py`)

### A. Prep Time Predictor (`estimate_prep_time_minutes`)
- **Base Overhead:** Starts at a baseline of 10 minutes for oven heating and packaging.
- **Item Complexity Accumulator:** Sums individual item preparation times (`mi.prep_minutes * quantity`).
- **Kitchen Load Penalty:** Queries current active orders (`received` or `preparing`) for the selected outlet and adds +3 minutes per queued order (capped at a maximum penalty of +25 minutes).
- **Business Rule Compliance:** Promised delivery/pickup time enforces `max(ai_estimate, outlet.minimum_prep_time)` as specified in the project brief.
- **Uncertainty Fallback:** If a menu item entry is unlisted or missing, safely defaults to 15 minutes per item.

### B. AI Reorder Recommender (`get_reorder_suggestions`)
- **Past Order Intelligence:** Analyzes authenticated user order history via Django ORM annotations (`Count('id')`) to identify their top 3 most frequently ordered dishes.
- **Cold-Start Fallback:** If the user has no previous order history (new user) or is unauthenticated, safely falls back to top globally ordered dishes across all outlets.
- **UX Guardrail:** Displays recommendations as optional suggestions and never auto-adds items to the user's cart without explicit consent.

---

## 5. UI & Design Decisions
- **Brand Identity:** Soft light saffron orange background (`#FFF0E5`) reflecting Hyderabadi biryani heritage.
- **User Roles:** Distinct user views for Customers (browsing, cart, order tracking) and Kitchen Staff (dark-mode high-contrast KDS with late alerts).
- **GST Disclosure:** Explicitly displays "Inclusive of 5% GST" on all cards and cart summaries.

---

## 6. Assumptions & Scope Cut
- **Assumptions Labeled:**
  - *Assumption 1:* Delivery radius is within 5 km of the selected outlet.
  - *Assumption 2:* Simulated payment gateway approves all valid card/UPI tests.
- **What Was Cut:** Real SMS gateway integration (simulated via on-screen order status updates).
- **Future Roadmap:** Multi-outlet inventory sync and automated WhatsApp order notifications.