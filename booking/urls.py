from django.urls import path
from .views import BookAppointmentView,ProfessionalBookingsAPIView,CompleteWorkView,UserAddConfirm

urlpatterns = [
    path('bookings/',BookAppointmentView.as_view(),name='bookings'),
    path('booking/<int:professional_id>/',BookAppointmentView.as_view(),name='booking'),
    path('professional_bookings/', ProfessionalBookingsAPIView.as_view(), name='professional-bookings-list'),
    path('professional_bookings/<int:booking_id>/<str:action>/', ProfessionalBookingsAPIView.as_view(), name='professional-booking-action'),
    path('complete_work/<int:booking_id>/', CompleteWorkView.as_view(), name='complete-work'),
    path('booking_details/<int:booking_id>/', UserAddConfirm.as_view(), name='booking-details'),



]