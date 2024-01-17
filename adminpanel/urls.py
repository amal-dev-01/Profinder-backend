from django.urls import path

from adminpanel.views import ProfessionlList, UserDetails, UserList,Total,send_mail_to_users

urlpatterns = [
    path("users/", UserList.as_view(), name="user-list"),
    path("professionals/", ProfessionlList.as_view(), name="professional-list"),
    path("details_view/<int:pk>/", UserDetails.as_view(), name="user-details"),
    path("total/", Total.as_view()),
    path('sendmail/', send_mail_to_users,name="send_mail_to_users"),
    # path('sendmailattime/', sendmailattime,name="sendmailattime"),





]
