from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import Booking
from adminpanel.models import Payment

@receiver(post_save, sender=Booking)
def create_payment(sender, instance, created, **kwargs):
    if instance.is_completed:
            amount = instance.price
            month = instance.booking_date.month
            year = instance.booking_date.year
            payment = Payment.objects.filter(
            professional=instance.professional,
            month=month,
            year=year).first()

            if payment:
                payment.amount += amount
                payment.save()
            else:
                Payment.objects.create(
                    professional=instance.professional,
                    month=month,
                    year=year,
                    amount=amount
                )

