from django.contrib import admin

# from django.contrib.gis.admin.options import OSMGeoAdmin
from django.contrib.gis.admin import GISModelAdmin

from account.models import Follower, Location, ProfessionalProfile, User, UserProfile

# from django.contrib.gis import gdal
# from django.contrib.gis.admin import OSMGeoAdmin


# Register your models here.


@admin.register(User)
class UserRegister(GISModelAdmin):
    list_display = ("email", "is_active", "is_professional", "is_admin")


@admin.register(UserProfile)
class UserProfiles(admin.ModelAdmin):
    list_display = ("user", "id")


@admin.register(ProfessionalProfile)
class ProfessionlProfile(admin.ModelAdmin):
    list_display = ("user", "job")


@admin.register(Location)
class LocationDetail(admin.ModelAdmin):
    list_display = ("user", "coordinates")


@admin.register(Follower)
class Follow(admin.ModelAdmin):
    list_display = (
        "user",
        "following_user",
    )
