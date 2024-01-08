from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models

# from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone = PhoneNumberField(region="IN")
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_exp = models.DateTimeField(blank=True, null=True)
    adhaar = models.CharField(max_length=12, blank=True, null=True)
    # followers = models.ManyToManyField("self", symmetrical=False, related_name="followings", blank=True)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_professional = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email}and {self.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    image = models.ImageField(
        default="default.jpg", upload_to="profile_pics", blank=True
    )
    bio = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.email


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="professionalprofile"
    )
    job = models.CharField(max_length=100, null=True)
    experience = models.IntegerField(null=True)
    skills = models.TextField(null=True)
    image = models.ImageField(
        default="default.jpg", upload_to="profile_pics", null=True
    )
    bio = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="location")
    coordinates = models.PointField(srid=4326, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    @property
    def longitude(self):
        return self.coordinates.x

    @property
    def latitude(self):
        return self.coordinates.y


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    created = models.DateTimeField(auto_now_add=True)
