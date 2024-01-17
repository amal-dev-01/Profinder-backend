from django.db import models
from account.models import User
# Create your models here.


class Payment(models.Model):
    professional = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for {self.professional.email} - {self.month}/{self.year}"