from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# User manager
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Vendor(models.Model):
    vendor_code = models.CharField(
        max_length=100, unique=True, primary_key=True, blank=False
    )
    name = models.CharField(max_length=200, help_text=('Vendor"s name.'))
    contact_details = models.TextField(help_text=("Contact information of the vendor."))
    address = models.TextField(help_text=("Physical address of the vendor."))
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.vendor_code} {self.name}"


class PurchaseOrder(models.Model):
    ORDER_STATUS = (
        ("pending", "pending"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
    )
    
    po_number = models.CharField(
        max_length=100, unique=True, primary_key=True, blank=False
    )
    vendor = models.ForeignKey(
        Vendor, related_name="purchase_order", on_delete=models.CASCADE
    )
    order_date = models.DateTimeField(blank=True , null=True)
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(choices=ORDER_STATUS, max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number}"

    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name="history_performance", on_delete=models.CASCADE
    )
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_average = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
