# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from account.models import ProfessionalProfile, User, UserProfile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_professional:
#                 ProfessionalProfile.objects.create(user=instance)
#         UserProfile.objects.create(user=instance)
#         # print(instance,'para')
#
