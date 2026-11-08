from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Outlet(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    fssai_number = models.CharField(max_length=50)
    delivery_radius_km = models.IntegerField(default=5)
    minimum_prep_time = models.IntegerField(default=25)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    SPICE_CHOICES = [
        ("mild", "Mild"),
        ("medium", "Medium"),
        ("hot", "Hot"),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    outlets = models.ManyToManyField(Outlet, related_name="menu_items")
    photo_url = models.URLField(
        blank=True,
        default="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&h=300&fit=crop",
    )
    is_veg = models.BooleanField(default=False)
    spice_level = models.CharField(
        max_length=10, choices=SPICE_CHOICES, default="medium"
    )
    allergens = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    prep_minutes = models.IntegerField(default=15)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.name} - Rs{self.price}"


class AddOn(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="addons"
    )

    def __str__(self):
        return f"{self.name} (+Rs{self.price})"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    loyalty_points = models.IntegerField(default=0)
    opt_in_marketing = models.BooleanField(default=False)
    preferred_outlet = models.ForeignKey(
        Outlet, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.user.username} ({self.phone})"


class Order(models.Model):
    STATUS_CHOICES = [
        ("received", "Received"),
        ("preparing", "Preparing"),
        ("ready", "Ready for Pickup"),
        ("handed_off", "Handed to Rider"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [
        ("upi", "UPI"),
        ("card", "Card"),
    ]
    order_id = models.CharField(max_length=20, unique=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, default="upi"
    )
    payment_status = models.CharField(max_length=20, default="paid")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="received")
    placed_at = models.DateTimeField(auto_now_add=True)
    promised_at = models.DateTimeField(null=True, blank=True)
    actual_ready_at = models.DateTimeField(null=True, blank=True)
    coupon_code = models.CharField(max_length=50, blank=True)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ["-placed_at"]

    def __str__(self):
        return f"{self.order_id} - {self.status}"

    def is_late(self):
        if self.status in ["delivered", "cancelled", "handed_off", "ready"]:
            return False
        if self.promised_at and timezone.now() > self.promised_at:
            return True
        return False

    def minutes_past_promise(self):
        if self.promised_at and timezone.now() > self.promised_at:
            return int((timezone.now() - self.promised_at).total_seconds() / 60)
        return 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    add_ons_text = models.CharField(max_length=500, blank=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"
