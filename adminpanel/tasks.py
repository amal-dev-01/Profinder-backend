from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from account.models import User
from profinder import settings
from adminpanel.models import Payment
from datetime import datetime,date


 	


@shared_task()
def send_mail_func():
    users = Payment.objects.filter(month=datetime.now().month, year=datetime.now().year)
    for user in users:
        subject ='Pay monthly subscription',
        message = f"Hi {user.professional.username},\n\nWe hope you're enjoying our services! This is a friendly reminder to pay your monthly subscription of ₹ {user.total_amount} to continue accessing our features.\n\nIf you've already made the payment, thank you! Otherwise, please make the payment at your earliest convenience to avoid any interruption in your service. Your continued support is highly appreciated.\n\nIf you have any questions or concerns, feel free to reach out to our support team.\n\nBest regards,\nThe Profinder Team"
        to_email = user.professional.email
        send_mail(subject, message, None, [to_email])
    return "Task Successfull"


@shared_task()
def over_due_block():
    overdue_professionals = User.objects.filter(
        is_professional =True,
        payment__status=Payment.PENDING,
        # payment__month__lt=(date.today().month-1),
        # payment__year=date.today().year
    )

    for professional in User.objects.filter(is_professional =True):
        if professional in overdue_professionals:
            professional.is_blocked = True
            message ="blocked"
            subject="bloceddddddddd"
            to_email=professional.email
            send_mail(subject, message, None, [to_email])
        else:
            professional.is_blocked = False

        professional.save()
    return "message Professionals blocked or unblocked based on payment status."


