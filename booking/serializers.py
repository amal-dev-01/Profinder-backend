from rest_framework import serializers
from account.models import Location,User,ProfessionalProfile


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['coordinates', 'country', 'state', 'district', 'city']

class ProfessionalProfileSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ("job", "experience", "skills", "image", "bio", "address")



class ProfessionalSearchSerializer(serializers.ModelSerializer):
    professionalprofile = ProfessionalProfileSerilaizer(required=False)
    location = LocationSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone",
            "first_name",
            "last_name",
            "professionalprofile",
            "location"
        )