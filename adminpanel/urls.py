from django.urls import path

from adminpanel.views import ProfessionlList, UserDetails, UserList

urlpatterns = [
    path("users/", UserList.as_view(), name="user-list"),
    path("professionals/", ProfessionlList.as_view(), name="professional-list"),
    path("details_view/<int:pk>/", UserDetails.as_view(), name="user-details"),
]
