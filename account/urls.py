from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import (
    ChangePasswordView,
    CurrentLocation,
    FollowersView,
    FollowUserView,
    ForgotPasswordView,
    MyObtainTokenPairView,
    ProfessionalRegisterView,
    RegisterView,
    ResendOtp,
    ResetPasswordView,
    SearchProfessionalsView,
    UserDetailAPIView,
    UserListToFollowView,
    VerifyOtp,
    ViewUserProfile,
    UserPostView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user_register"),
    path("pro/", ProfessionalRegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOtp.as_view(), name="register_otp"),
    path("resend-otp/", ResendOtp.as_view(), name="resend-otp"),
    path("token/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("userprofile/", UserDetailAPIView.as_view(), name="userprofile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "forgot-password/", ForgotPasswordView.as_view(), name="password-reset-request"
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path("location/", CurrentLocation.as_view(), name="current-location"),
    path("<int:pk>/follow/", FollowUserView.as_view(), name="follow"),
    path("<int:user_id>/unfollow/", FollowUserView.as_view(), name="unfollow"),
    path("userlist/", UserListToFollowView.as_view(), name="follow-toggle"),
    path("followlist/", FollowersView.as_view(), name="user-following"),
    path("search/", SearchProfessionalsView.as_view(), name="search_professionals"),
    path("user_post/<int:pk>/", UserPostView.as_view(), name="user_post"),

    path(
        "user_view/<int:pk>/",
        ViewUserProfile.as_view(),
        name="user-details",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
