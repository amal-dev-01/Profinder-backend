from django.contrib.auth import get_user_model
from rest_framework import serializers

# from rest_framework.validators import UniqueValidator
# from rest_framework_gis.serializers import GeoFeatureModelListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import Follower, Location, ProfessionalProfile, User, UserProfile

# from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    # write_only=True, required=True,
    # validators=[validate_password]
    # )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "phone")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfessionalRegisterSerializer(serializers.ModelSerializer):
    adhaar = serializers.CharField(max_length=12, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "phone", "adhaar")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        user = get_user_model().objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["is_admin"] = user.is_admin
        token["is_active"] = user.is_active
        token["is_professional"] = user.is_professional
        token["is_user"] = user.is_user
        return token


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ProfessionalProfileSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalProfile
        fields = ("job", "experience", "skills", "image", "bio", "address")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("image", "bio", "address")


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(required=False)
    professionalprofile = ProfessionalProfileSerilaizer(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone",
            "first_name",
            "last_name",
            "userprofile",
            "professionalprofile",
            "is_active",
        )

    def update(self, instance, validated_data):
        # is_professional = instance.is_professional
        # print(is_professional)
        # print(profile_data)
        # profile = instance.userprofile
        # professional = instance.professionalprofile
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        try:
            professional_data = validated_data.pop("professionalprofile", {})
            professional = instance.professionalprofile
            professional.image = professional_data.get("image", professional.image)
            professional.bio = professional_data.get("bio", professional.bio)
            professional.address = professional_data.get(
                "address", professional.address
            )
            professional.job = professional_data.get("job", professional.job)
            professional.skills = professional_data.get("skills", professional.skills)
            professional.experience = professional_data.get(
                "experience", professional.experience
            )
            professional.save()
        except:
            profile = instance.userprofile
            profile_data = validated_data.pop("userprofile", {})
            profile.image = profile_data.get("image", profile.image)
            profile.bio = profile_data.get("bio", profile.bio)
            profile.address = profile_data.get("address", profile.address)
            profile.save()

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class FollowerSerializer(serializers.ModelSerializer):
    user = UserFollowSerializer()
    following_user = UserFollowingSerializer()

    class Meta:
        model = Follower
        fields = ["id", "created", "user", "following_user"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
