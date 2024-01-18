from django.db import models
from account.models import User
# Create your models here.


class Payment(models.Model):
    PENDING = "pending"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        ]
    professional = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_id = models.CharField(max_length=255, null = True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)



    def __str__(self):
        return f"Payment for {self.professional.email} - {self.month}/{self.year}"
    


