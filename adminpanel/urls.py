from django.urls import path,include
from adminpanel.views import UserList,UserDetails,ProfessionlList


urlpatterns = [


    path('users/', UserList.as_view(), name='user-list'),
    path('professionals/', ProfessionlList.as_view(), name='professional-list'),
    path('details_view/<int:pk>/', UserDetails.as_view(), name='user-details'),
]