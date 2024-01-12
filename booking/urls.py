from django.urls import path
from booking.views import UserSearchView

urlpatterns = [
path('search/', UserSearchView.as_view(), name='search_professionals'),

]