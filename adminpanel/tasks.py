from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from account.models import User
from profinder import settings
from adminpanel.models import Payment
from datetime import datetime


 	


@shared_task()
def send_mail_func():
    users = Payment.objects.filter(month=datetime.now().month, year=datetime.now().year)
    for user in users:
        subject ='Pay monthly subscription',
        message = f"Hi {user.professional.username},\n\nWe hope you're enjoying our services! This is a friendly reminder to pay your monthly subscription of ₹ {user.total_amount} to continue accessing our features.\n\nIf you've already made the payment, thank you! Otherwise, please make the payment at your earliest convenience to avoid any interruption in your service. Your continued support is highly appreciated.\n\nIf you have any questions or concerns, feel free to reach out to our support team.\n\nBest regards,\nThe Profinder Team"
        to_email = user.professional.email
        send_mail(subject, message, None, [to_email])
    return "Task Successfull"
