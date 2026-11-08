from django.contrib import messages
import json
import random
from decimal import Decimal
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone

from .models import Outlet, Category, MenuItem, Order, OrderItem, CustomerProfile
from .ai import estimate_prep_time_minutes, get_reorder_suggestions


# ── AUTH ──────────────────────────────────────────────


def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect("kitchen_display")

            # If they clicked "Login to order" from a specific outlet
            next_url = request.GET.get("next", "outlet_select")
            return redirect(next_url)

        error = "Invalid username or password"
    return render(request, "core/login.html", {"error": error})


def register_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        if User.objects.filter(username=username).exists():
            error = "Username already taken"
        elif len(password) < 4:
            error = "Password too short"
        else:
            user = User.objects.create_user(username=username, password=password)
            CustomerProfile.objects.create(user=user, phone=phone)
            login(request, user)
            return redirect("outlet_select")
    return render(request, "core/login.html", {"error": error, "register": True})


def logout_view(request):
    logout(request)
    return redirect("home")


# ── CUSTOMER FLOW ─────────────────────────────────────


# REMOVED @login_required here so ANYONE can see the homepage!
def outlet_select(request):
    outlets = Outlet.objects.filter(is_active=True)
    return render(request, "core/landing.html", {"outlets": outlets})


@login_required
def menu_view(request, outlet_id):
    outlet = get_object_or_404(Outlet, id=outlet_id, is_active=True)
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(outlets=outlet, is_available=True)

    request.session["outlet_id"] = outlet.id

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values()) if cart else 0

    return render(
        request,
        "core/menu.html",
        {
            "outlet": outlet,
            "categories": categories,
            "menu_items": menu_items,
            "cart_count": cart_count,
        },
    )


@login_required
def add_to_cart(request):
    if request.method == "POST":
        item_id = str(request.POST.get("item_id") or request.POST.get("menu_item_id") or "")
        if item_id and item_id != "None":
            cart = request.session.get("cart")
            if not isinstance(cart, dict):
                cart = {}
            cart[item_id] = int(cart.get(item_id, 0)) + 1
            request.session["cart"] = cart
            request.session.modified = True
            
            try:
                mi = MenuItem.objects.get(id=int(item_id))
                messages.success(request, f"✅ Added '{mi.name}' to cart! (Total items in cart: {sum(cart.values())})")
            except Exception:
                messages.success(request, "✅ Item added to cart!")
    return redirect(request.META.get("HTTP_REFERER", "/"))
@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    item_id = str(item_id)
    if item_id in cart:
        cart[item_id] -= 1
        if cart[item_id] <= 0:
            del cart[item_id]
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart_view")


@login_required
def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0")

    for item_id, qty in cart.items():
        try:
            mi = MenuItem.objects.get(id=int(item_id))
            subtotal = mi.price * qty
            items.append({"menu_item": mi, "quantity": qty, "subtotal": subtotal})
            total += subtotal
        except MenuItem.DoesNotExist:
            continue

    suggestions = get_reorder_suggestions(request.user)

    outlet_id = request.session.get("outlet_id")
    outlet = Outlet.objects.filter(id=outlet_id).first() if outlet_id else None

    return render(
        request,
        "core/cart.html",
        {
            "items": items,
            "total": total,
            "suggestions": suggestions,
            "outlet": outlet,
        },
    )


@login_required
def checkout_view(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart_view")

    outlet_id = request.session.get("outlet_id")
    if not outlet_id:
        return redirect("outlet_select")
    outlet = get_object_or_404(Outlet, id=outlet_id)

    items_data = []
    total = Decimal("0")
    for item_id, qty in cart.items():
        try:
            mi = MenuItem.objects.get(id=int(item_id))
            items_data.append({"menu_item": mi, "quantity": qty})
            total += mi.price * qty
        except MenuItem.DoesNotExist:
            continue

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "upi")
        coupon = request.POST.get("coupon", "").strip().upper()
        discount = Decimal("0")
        if coupon == "BIRYANI10":
            discount = total * Decimal("0.10")

        final_total = total - discount

        # Calculate AI prep time
        cart_for_ai = [
            {"menu_item_id": int(i["menu_item"].id), "quantity": i["quantity"]}
            for i in items_data
        ]
        prep_minutes = estimate_prep_time_minutes(outlet, cart_for_ai)
        promised_at = timezone.now() + timedelta(minutes=prep_minutes)

        # Generate unique order ID
        order_id = f"WEB-{random.randint(100000, 999999)}"
        while Order.objects.filter(order_id=order_id).exists():
            order_id = f"WEB-{random.randint(100000, 999999)}"

        order = Order.objects.create(
            order_id=order_id,
            outlet=outlet,
            customer=request.user,
            total=final_total,
            payment_method=payment_method,
            payment_status="paid",
            status="received",
            promised_at=promised_at,
            coupon_code=coupon,
            discount=discount,
        )

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                menu_item=item["menu_item"],
                quantity=item["quantity"],
                unit_price=item["menu_item"].price,
            )

        # Loyalty points calculation
        try:
            profile = request.user.customerprofile
            profile.loyalty_points += int(final_total // 10)
            profile.save()
        except CustomerProfile.DoesNotExist:
            pass

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("order_status", order_id=order_id)

    return render(
        request,
        "core/checkout.html",
        {
            "items": items_data,
            "total": total,
            "outlet": outlet,
        },
    )


@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, customer=request.user)
    items = order.items.select_related("menu_item").all()
    return render(
        request,
        "core/order_status.html",
        {
            "order": order,
            "items": items,
        },
    )


# ── KITCHEN DISPLAY ──────────────────────────────────


@login_required
def kitchen_display(request):
    outlets = Outlet.objects.filter(is_active=True)
    selected_outlet_id = request.GET.get("outlet")
    if selected_outlet_id:
        request.session["kitchen_outlet"] = int(selected_outlet_id)

    kitchen_outlet_id = request.session.get("kitchen_outlet")
    outlet = None
    orders = []

    if kitchen_outlet_id:
        outlet = Outlet.objects.filter(id=kitchen_outlet_id).first()
        if outlet:
            orders = (
                Order.objects.filter(outlet=outlet)
                .exclude(status__in=["delivered", "cancelled"])
                .prefetch_related("items__menu_item")[:20]
            )

    return render(
        request,
        "core/kitchen_display.html",
        {
            "outlets": outlets,
            "outlet": outlet,
            "orders": orders,
        },
    )


@login_required
def kitchen_api_orders(request):
    outlet_id = request.GET.get("outlet")
    if not outlet_id:
        return JsonResponse({"orders": []})

    orders = (
        Order.objects.filter(outlet_id=outlet_id)
        .exclude(status__in=["delivered", "cancelled"])
        .prefetch_related("items__menu_item")[:20]
    )

    data = []
    for o in orders:
        items_text = ", ".join(
            [f"{i.menu_item.name} x{i.quantity}" for i in o.items.all()]
        )
        data.append(
            {
                "order_id": o.order_id,
                "status": o.status,
                "status_display": o.get_status_display(),
                "items": items_text,
                "total": str(o.total),
                "placed_at": o.placed_at.strftime("%H:%M"),
                "promised_at": o.promised_at.strftime("%H:%M") if o.promised_at else "",
                "is_late": o.is_late(),
                "minutes_late": o.minutes_past_promise(),
            }
        )

    return JsonResponse({"orders": data})


@login_required
def kitchen_update_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, order_id=order_id)
        new_status = request.POST.get("status")
        valid = [
            "received",
            "preparing",
            "ready",
            "handed_off",
            "delivered",
            "cancelled",
        ]
        if new_status in valid:
            order.status = new_status
            if new_status == "ready":
                order.actual_ready_at = timezone.now()
            order.save()
    return redirect("kitchen_display")


# ── API FOR CUSTOMER ORDER STATUS ─────────────────────


@login_required
def order_status_api(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return JsonResponse(
        {
            "status": order.status,
            "status_display": order.get_status_display(),
            "is_late": order.is_late(),
        }
    )
