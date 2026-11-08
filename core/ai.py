from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, MenuItem


def estimate_prep_time_minutes(outlet, cart_items):
    """
    AI Prep Time Predictor:
    Calculates estimated preparation time based on item complexity
    and current kitchen load for the selected outlet.
    Per brief: Promised time is max(AI estimate, outlet minimum).
    """
    base_time = 10

    item_time = 0
    for ci in cart_items:
        try:
            mi = MenuItem.objects.get(id=ci["menu_item_id"])
            item_time += mi.prep_minutes * ci["quantity"]
        except MenuItem.DoesNotExist:
            item_time += 15 * ci["quantity"]

    # Kitchen load penalty: add 3 mins per currently active order
    active_orders = Order.objects.filter(
        outlet=outlet, status__in=["received", "preparing"]
    ).count()
    load_penalty = min(active_orders * 3, 25)

    ai_estimate = base_time + item_time + load_penalty

    # Rule from brief: "promised time is the higher of the AI estimate and the outlet's minimum"
    return max(ai_estimate, outlet.minimum_prep_time)


def get_reorder_suggestions(user, limit=3):
    """
    AI Reorder Recommender:
    Suggests items from customer's past order history.
    Per brief: Suggestions never auto-add items to cart.
    """
    if not user.is_authenticated:
        return []

    past_items = (
        OrderItem.objects.filter(order__customer=user)
        .values(
            "menu_item_id",
            "menu_item__name",
            "menu_item__price",
            "menu_item__photo_url",
        )
        .annotate(times_ordered=models.Count("id"))
        .order_by("-times_ordered")[:limit]
    )

    if not past_items:
        # Fallback to globally popular items
        past_items = (
            OrderItem.objects.values(
                "menu_item_id",
                "menu_item__name",
                "menu_item__price",
                "menu_item__photo_url",
            )
            .annotate(times_ordered=models.Count("id"))
            .order_by("-times_ordered")[:limit]
        )

    return list(past_items)
