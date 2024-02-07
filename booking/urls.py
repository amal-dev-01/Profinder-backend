from django.urls import include, path

from .routing import websocket_urlpatterns
from .views import (
    BookAppointmentView,
    BookingData,
    CompleteWorkView,
    Notification,
    ProfessionalAcceptBookingsAPIView,
    ProfessionalBookingsAPIView,
    UserAddConfirm,
)

urlpatterns = [
    path("bookings/", BookAppointmentView.as_view(), name="bookings"),
    path(
        "booking/<int:professional_id>/", BookAppointmentView.as_view(), name="booking"
    ),
    path(
        "professional_bookings/",
        ProfessionalBookingsAPIView.as_view(),
        name="professional-bookings-list",
    ),
    path(
        "professional_bookings_accepted/",
        ProfessionalAcceptBookingsAPIView.as_view(),
        name="professional-bookings-accept",
    ),
    path(
        "professional_bookings/<int:booking_id>/<str:action>/",
        ProfessionalBookingsAPIView.as_view(),
        name="professional-booking-action",
    ),
    path(
        "complete_work/<int:booking_id>/",
        CompleteWorkView.as_view(),
        name="complete-work",
    ),
    path(
        "booking_details/<int:booking_id>/",
        UserAddConfirm.as_view(),
        name="booking-details",
    ),
    path(
        "booking_details/<int:booking_id>/<str:action>/",
        UserAddConfirm.as_view(),
        name="booking-details",
    ),
    path("ws/", include(websocket_urlpatterns)),
    path(
        "notification/",
        Notification.as_view(),
        name="notification",
    ),
    path("booking_cache/", BookingData.as_view()),
]
