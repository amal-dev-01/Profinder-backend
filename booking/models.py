from django.contrib.gis.db import models

from account.models import User


# Create your models here.
class Booking(models.Model):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELED = "canceled"
    INCOMPLETED = "Incompleted"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (COMPLETED, "Completed"),
        (CANCELED, "Canceled"),
        (INCOMPLETED, "Incompleted"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booked_appointments"
    )
    booking_date = models.DateTimeField()
    address = models.TextField()
    job = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email} to {self.professional.email} on {self.booking_date}"


class Complaint(models.Model):
    PENDING = "pending"
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (OPEN, "Open"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
