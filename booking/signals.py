# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from asgiref.sync import async_to_sync
# from .models import BookingNotification
# from django.http import JsonResponse
# from channels.layers import get_channel_layer


# @receiver(post_save, sender=BookingNotification)
# def notification_created(sender, instance, created, **kwargs):
#     if created:
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 'notifications_group',
#                 {
#                     'type': 'send_notification',
#                     'message': 'New notification!',
#                 }
#             )
#             return JsonResponse({'status': 'Notification sent!'})
