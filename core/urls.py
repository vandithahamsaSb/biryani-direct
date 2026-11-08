from django.urls import path
from . import views

urlpatterns = [
    path("", views.outlet_select, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("outlet/", views.outlet_select, name="outlet_select"),
    path("menu/<int:outlet_id>/", views.menu_view, name="menu"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_view, name="cart_view"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("order/<str:order_id>/", views.order_status, name="order_status"),
    path("order/<str:order_id>/api/", views.order_status_api, name="order_status_api"),
    path("kitchen/", views.kitchen_display, name="kitchen_display"),
    path("kitchen/api/", views.kitchen_api_orders, name="kitchen_api"),
    path(
        "kitchen/<str:order_id>/update/",
        views.kitchen_update_status,
        name="kitchen_update",
    ),
]
