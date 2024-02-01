import json
import urllib

from django.contrib.auth.tokens import default_token_generator
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ipware import get_client_ip
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import Follower, Location, ProfessionalProfile, User, UserProfile
from account.serializers import LocationSerializer
from posts.models import Post
from .serializers import (
    ChangePasswordSerializer,
    FollowerSerializer,
    ForgotPasswordSerializer,
    MyTokenObtainPairSerializer,
    OTPVerificationSerializer,
    ProfessionalRegisterSerializer,
    RegisterSerializer,
    ResendOtpSerializer,
    UserListSerializer,
    UserSerializer,
)
from posts.serializer import PostSerializer
from .utils import generate_otp

# Create your views here.


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            user.otp = otp
            print(f"user otp {otp}")
            user.otp_exp = timezone.now() + timezone.timedelta(minutes=1)
            user.is_user = True
            user.is_active = False
            user.save()
            # subject = 'Registration OTP'
            # message = f'Your OTP for registration is: {otp}'
            # to_email = user.email
            # send_mail(subject, message, None, [to_email])
            return Response({"message": "Otp sended"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessionalRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = ProfessionalRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            user.otp = otp
            print(f"user otp {otp}")
            user.otp_exp = timezone.now() + timezone.timedelta(minutes=5)
            user.is_professional = True
            user.is_active = False
            user.save()
            # subject = 'Registration OTP'
            # message = f'Your OTP for registration is: {otp}'
            # to_email = user.email
            # send_mail(subject, message, None, [to_email])
            return Response({"message": "Otp sended"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            submitted_otp = serializer.validated_data["otp"]

            try:
                user = User.objects.get(email=email)

                if submitted_otp == user.otp and timezone.now() < user.otp_exp:
                    user.is_active = True
                    user.save()
                    if user.is_professional:
                        ProfessionalProfile.objects.create(user=user)
                    else:
                        UserProfile.objects.create(user=user)

                    return Response(
                        {"msg": "OTP verified successfully."}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
                    )

            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOtp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = ResendOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            if user.otp_exp and timezone.now() < user.otp_exp:
                time_remaining = (user.otp_exp - timezone.now()).total_seconds()
                return Response(
                    {
                        "error": f"Wait for {time_remaining} minutes before requesting a new OTP."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_otp = generate_otp()
            user.otp = new_otp
            user.otp_exp = user.otp_exp = timezone.now() + timezone.timedelta(minutes=1)
            user.save()
            subject = "Registration OTP (Resent)"
            message = f"Your new OTP for registration is: {new_otp}"
            to_email = user.email
            send_mail(subject, message, None, [to_email])

            return Response(
                {"msg": "New OTP sent. Check your email."}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            raise ValidationError(serializer.errors)

        except ValidationError as validation_error:
            return Response(
                {"error": "Validation error", "detail": validation_error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        password = serializer.validated_data["password"]

        if not request.user.check_password(old_password):
            return Response(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(password)
        request.user.save()
        return Response(
            {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
        )


class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://127.0.0.1:8000/reset-password/{uidb64}/{token}/"
        subject = "Forgot Password"
        message = f"Click the link to reset your password: {reset_link}"
        to_email = user.email
        send_mail(subject, message, None, [to_email])
        return Response(
            {"detail": "Password reset email sent successfully"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    def put(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            new_password = request.data.get("new_password")

            if new_password:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"detail": "Password reset successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"new_password": "This field is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST
            )

class ViewUserProfile(APIView):
    def get(self,request,pk):
        user = User.objects.get(pk=pk)
        serializer =UserSerializer(user)
        return Response(serializer.data)


class UserPostView(APIView):
    def get(self,request,pk):
        posts = Post.objects.filter(user=pk)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CurrentLocation(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        client_ip, is_routable = get_client_ip(request)

        if client_ip is None:
            client_ip = "0.0.0.0"
        else:
            if is_routable:
                ip_type = "public"
            else:
                ip_type = "private"

        ip_address = "103.70.197.218"
        url = "https://api.ipfind.com/?ip=" + ip_address
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        data1["client_ip"] = client_ip
        data1["ip_type"] = ip_type
        coordinates = Point(data1["longitude"], data1["latitude"], srid=4326)
        if (
            Q(data1["country"])
            & Q(data1["city"])
            & Q(data1["region"])
            & Q(data1["county"])
        ):
            location, created = Location.objects.get_or_create(user=request.user)
            coordinates = Point(data1["longitude"], data1["latitude"], srid=4326)
            location.country = data1["country"]
            print(location.country)
            location.state = data1["region"]
            location.district = data1["county"]
            location.city = data1["city"]
            location.coordinates = coordinates
            location.save()
        return Response(data1, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        user_to_follow = get_object_or_404(User, id=pk)
        if Follower.objects.filter(
            user=request.user, following_user=user_to_follow
        ).exists():
            return Response(
                {"message": "User is already being followed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follower.objects.create(user=request.user, following_user=user_to_follow)
        return Response(
            {"message": "User followed successfully"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id=None):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if not Follower.objects.filter(
            user=request.user, following_user=user_to_unfollow
        ).exists():
            return Response(
                {"message": "User is not being followed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follower.objects.filter(
            user=request.user, following_user=user_to_unfollow
        ).delete()
        return Response(
            {"message": "User unfollowed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class FollowersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        followers = Follower.objects.filter(following_user=user)
        following = Follower.objects.filter(user=user)
        followers_serializer = FollowerSerializer(followers, many=True)
        following_serializer = FollowerSerializer(following, many=True)

        data = {
            "followers": followers_serializer.data,
            "following": following_serializer.data,
            "followers_count": followers.count(),
            "following_count": following.count(),
        }

        return Response(data)


class UserListToFollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        users_to_follow = User.objects.exclude(id=request.user.id)
        users_to_follow = users_to_follow.exclude(followers__id=request.user.id)
        serializer = UserListSerializer(users_to_follow, many=True)
        return Response(serializer.data)


class SearchProfessionalsView(APIView):
    def get(self, request, *args, **kwargs):
        job_title = request.query_params.get("job_title", "")
        locations = request.query_params.get("location", "")
        user_location = request.user.location.first()
        if user_location is not None:
            queryset = (
                Location.objects.filter(
                    user__professionalprofile__job__icontains=job_title,
                    city__icontains=locations,
                )
                .annotate(
                    distance=Distance(
                        "coordinates",
                        Point(
                            user_location.coordinates.x,
                            user_location.coordinates.y,
                            srid=4326,
                        ),
                    )
                )
                .order_by("distance")
            )

            serializer = LocationSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User has no associated locations"},
                status=status.HTTP_404_NOT_FOUND,
            )


# from django.shortcuts import get_object_or_404


# class UserFollowingView(APIView):
#     permission_classes =(IsAuthenticated,)
#     def get(self, request, pk, format=None):
#         user = get_object_or_404(User, pk=pk)
#         following = user.followings.all()
#         serializer = UserFollowingSerializer(following, many=True)
#         return Response(serializer.data)

# class UserFollowersView(APIView):
#     permission_classes =(IsAuthenticated,)
#     def get(self, request, pk, format=None):
#         user = get_object_or_404(User, pk=pk)
#         followers = user.followers.all()
#         serializer = UserFollowersSerializer(followers, many=True)
#         return Response(serializer.data)

# class FollowToggleView(APIView):
#     permission_classes =(IsAuthenticated,)

#     def post(self, request, pk, format=None):
#         user_to_follow = get_object_or_404(User, pk=pk)
#         if request.user in user_to_follow.followers.all():
#             user_to_follow.followers.remove(request.user)
#             message = 'Unfollowed successfully.'
#         else:
#             user_to_follow.followers.add(request.user)
#             message = 'Followed successfully.'

#         return Response({'message': message}, status=status.HTTP_200_OK)


# class Following(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         try:
#             user = request.user
#             following = user.followings.all()
#             serializer = UserFollowingSerializer(following, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class Follower(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         user = request.user
#         followers = user.followers.all()
#         serializer = UserFollowersSerializer(followers, many=True)
#         return Response(serializer.data)


# class RegisterView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             try:
#                 verification_sid = send_sms(str(user.phone))
#                 request.session['verification_sid']=verification_sid
#                 print(verification_sid)
#                 return Response ({'id':verification_sid},status=status.HTTP_200_OK)
#             except Exception as e:
#                 print(e)
#             return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)

#         print('llllllllll')
#         serializer.is_valid()
#         print(serializer['email'])
#         # try:
#         user = User.objects.create(
#             email=serializer.validated_data.get('email'),
#             username=serializer.validated_data.get('username'),
#             password=serializer.validated_data.get('password'),
#             phone=serializer.validated_data.get('phone'),
#             is_professional=serializer.validated_data.get('is_professional', False),
#         )
#         print(user)
#         otp = generate_otp()
#         print(otp)
#         user.otp = otp
#         user.save()
#         print(otp)
#             # subject = 'Registration OTP'
#             # message = f'Your OTP for registration is: {otp}'
#             # to_email = user.email
#             # send_mail(subject, message, None, [to_email])
#         return Response({'msg': 'data inserted'}, status=status.HTTP_201_CREATED)
#         # except serializers.ValidationError as e:
#         #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         # except Exception as e:
#         #     return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
