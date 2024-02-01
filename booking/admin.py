from django.contrib import admin

from .models import Booking, Complaint,BookingNotification

# Register your models here.

admin.site.register(Booking)
admin.site.register(Complaint)
admin.site.register(BookingNotification)

