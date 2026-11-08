from django.contrib import admin
from .models import Outlet, Category, MenuItem, AddOn, CustomerProfile, Order, OrderItem


class AddOnInline(admin.TabularInline):
    model = AddOn
    extra = 1


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "fssai_number", "delivery_radius_km", "is_active"]
    list_filter = ["city", "is_active"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "display_order"]
    ordering = ["display_order"]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "is_veg",
        "spice_level",
        "is_available",
    ]
    list_filter = ["category", "is_veg", "is_available", "outlets"]
    list_editable = ["price", "is_available"]
    filter_horizontal = ["outlets"]
    inlines = [AddOnInline]
    search_fields = ["name"]


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "loyalty_points", "opt_in_marketing"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["menu_item", "quantity", "unit_price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "outlet",
        "customer",
        "total",
        "status",
        "placed_at",
        "promised_at",
    ]
    list_filter = ["status", "outlet", "payment_method"]
    list_editable = ["status"]
    readonly_fields = ["order_id", "placed_at"]
    inlines = [OrderItemInline]
    search_fields = ["order_id"]
