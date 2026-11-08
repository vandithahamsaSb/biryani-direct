"""
Seed Script: Populates realistic database data required by the brief.
Includes Outlets, Categories, Menu Items, Users, and Sample Orders.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biryani.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Outlet, Category, MenuItem, Order, OrderItem, CustomerProfile
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

print("🌱 Seeding database with brief sample data...")

# 1. Create Outlets
outlets_data = [
    (
        "Kondapur Outlet",
        "Hyderabad",
        "Plot 45, Kondapur Main Road",
        "13612345000123",
        6,
        25,
    ),
    (
        "Gachibowli Cloud Kitchen",
        "Hyderabad",
        "Tower B, Gachibowli IT Park",
        "13612345000456",
        4,
        20,
    ),
    (
        "Kukatpally Outlet",
        "Hyderabad",
        "KPHB Colony, Road No. 1",
        "13612345000789",
        7,
        30,
    ),
    (
        "Madhapur Express",
        "Hyderabad",
        "Jubilee Hills Check Post",
        "13612345000321",
        5,
        22,
    ),
]
outlets = []
for name, city, addr, fssai, radius, min_prep in outlets_data:
    o, _ = Outlet.objects.get_or_create(
        name=name,
        defaults={
            "city": city,
            "address": addr,
            "fssai_number": fssai,
            "delivery_radius_km": radius,
            "minimum_prep_time": min_prep,
        },
    )
    outlets.append(o)

# 2. Create Categories
cats_data = ["Biryani", "Starters", "Curries", "Breads", "Desserts", "Beverages"]
cats = []
for i, name in enumerate(cats_data):
    c, _ = Category.objects.get_or_create(name=name, defaults={"display_order": i})
    cats.append(c)

# 3. Create Menu Items
menu_data = [
    (
        "Chicken Dum Biryani",
        "Slow-cooked basmati rice with tender chicken, saffron and fried onions",
        299,
        cats[0],
        False,
        "hot",
        "gluten",
        20,
        "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&h=300&fit=crop",
    ),
    (
        "Chicken Dum Biryani Family Pack",
        "Feeds 4. Slow-cooked with extra raita and salan",
        899,
        cats[0],
        False,
        "hot",
        "gluten, dairy",
        30,
        "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&h=300&fit=crop",
    ),
    (
        "Mutton Biryani",
        "Premium goat meat layered with aged basmati",
        399,
        cats[0],
        False,
        "hot",
        "gluten",
        25,
        "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=400&h=300&fit=crop",
    ),
    (
        "Veg Biryani",
        "Paneer, vegetables and mint in fragrant rice",
        229,
        cats[0],
        True,
        "medium",
        "dairy",
        15,
        "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop",
    ),
    (
        "Mutton Haleem",
        "Slow-cooked wheat, lentils and mutton — Hyderabadi special",
        349,
        cats[0],
        False,
        "medium",
        "gluten, nuts",
        35,
        "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400&h=300&fit=crop",
    ),
    (
        "Chicken 65",
        "Spicy deep-fried chicken bites with curry leaves",
        249,
        cats[1],
        False,
        "hot",
        "gluten",
        12,
        "https://images.unsplash.com/photo-1610057099443-fde6c99db7f4?w=400&h=300&fit=crop",
    ),
    (
        "Paneer Tikka",
        "Grilled cottage cheese with peppers and onions",
        199,
        cats[1],
        True,
        "medium",
        "dairy",
        10,
        "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop",
    ),
    (
        "Mirchi Ka Salan",
        "Green chilli curry in peanut-sesame gravy",
        149,
        cats[2],
        True,
        "hot",
        "nuts, gluten",
        10,
        "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop",
    ),
    (
        "Double Ka Meetha",
        "Hyderabadi bread pudding with rabdi",
        129,
        cats[4],
        True,
        "mild",
        "dairy, gluten, nuts",
        8,
        "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=300&fit=crop",
    ),
]

menu_items = []
for name, desc, price, cat, veg, spice, allergens, prep, photo in menu_data:
    mi, _ = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            "description": desc,
            "price": Decimal(str(price)),
            "category": cat,
            "is_veg": veg,
            "spice_level": spice,
            "allergens": allergens,
            "prep_minutes": prep,
            "photo_url": photo,
        },
    )
    mi.outlets.set(outlets)
    menu_items.append(mi)

# 4. Create Demo Users
cust_user, created = User.objects.get_or_create(
    username="customer1", defaults={"email": "customer@test.com"}
)
if created:
    cust_user.set_password("test1234")
    cust_user.save()
    CustomerProfile.objects.create(
        user=cust_user, phone="+91 98765 43210", loyalty_points=120
    )

kitchen_user, created = User.objects.get_or_create(
    username="kitchen1", defaults={"email": "kitchen@test.com", "is_staff": True}
)
if created:
    kitchen_user.set_password("test1234")
    kitchen_user.save()

admin_user, created = User.objects.get_or_create(
    username="admin",
    defaults={"email": "admin@test.com", "is_staff": True, "is_superuser": True},
)
if created:
    admin_user.set_password("admin1234")
    admin_user.save()

# 5. Create Sample Orders from Brief (WEB-778120, WEB-778131, WEB-778146)
now = timezone.now()
orders_data = [
    (
        "WEB-778120",
        outlets[0],
        cust_user,
        [(menu_items[1], 1), (menu_items[8], 2)],
        1180,
        "upi",
        "preparing",
        now - timedelta(minutes=20),
        now + timedelta(minutes=25),
    ),
    (
        "WEB-778131",
        outlets[1],
        cust_user,
        [(menu_items[3], 2), (menu_items[7], 1)],
        640,
        "card",
        "ready",
        now - timedelta(minutes=30),
        now + timedelta(minutes=5),
    ),
    (
        "WEB-778146",
        outlets[2],
        cust_user,
        [(menu_items[4], 3)],
        1050,
        "upi",
        "preparing",
        now - timedelta(minutes=50),
        now - timedelta(minutes=4),
    ),
]

for oid, outlet, cust, items, total, pay, status, placed, promised in orders_data:
    order, created = Order.objects.get_or_create(
        order_id=oid,
        defaults={
            "outlet": outlet,
            "customer": cust,
            "total": Decimal(str(total)),
            "payment_method": pay,
            "payment_status": "paid",
            "status": status,
            "placed_at": placed,
            "promised_at": promised,
        },
    )
    if created:
        for mi, qty in items:
            OrderItem.objects.create(
                order=order, menu_item=mi, quantity=qty, unit_price=mi.price
            )

print("🎉 Seeding complete! Database successfully populated.")
