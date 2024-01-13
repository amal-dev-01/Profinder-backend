from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Message(models.Model):
    username = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = "chat_message"
        ordering = ("timestamp",)
