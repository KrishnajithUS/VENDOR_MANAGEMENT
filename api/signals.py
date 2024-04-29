from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from common.models import PurchaseOrder
from django.db.models import F


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if instance.pk:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        # Calculate On-Time Delivery Rate
        # Prevent Duplicate computations
        if instance.status == "completed":
            completed_on_time = completed_pos.filter(
                actual_delivery_date__lte=F("expected_delivery_date")
            ).count()
            total_completed_pos = completed_pos.count()
            vendor.on_time_delivery_rate = (
                completed_on_time / total_completed_pos
                if total_completed_pos > 0
                else 0
            )
        # Calculate Quality Rating Average
        if instance.status == "completed" and instance.quality_rating is not None:
            vendor_quality_avg = completed_pos.filter(
                quality_rating__isnull=False
            ).aggregate(avg_quality=Avg("quality_rating"))["avg_quality"]
            vendor.quality_rating_avg = (
                vendor_quality_avg if vendor_quality_avg is not None else 0
            )

        # Calculate Average Response Time
        if instance.acknowledgment_date:
            response_times = PurchaseOrder.objects.filter(
                vendor=instance.vendor, acknowledgment_date__isnull=False
            ).aggregate(
                avg_response_time=Avg(F("acknowledgment_date") - F("issue_date"))
            )
            vendor.average_response_time = response_times[
                "avg_response_time"
            ].total_seconds()
        # Prevent from calling post save again
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_pos = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed"
    ).count()
    vendor.fulfillment_rate = fulfilled_pos / total_pos if total_pos > 0 else 0

    vendor.save()
