from django.urls import path

from adminpanel.views import ProfessionlList, UsersDetailsView, UserList,Total,BookingView,BookingFilterView,BookingDetails,AdminPayment,PaymentSuccessView

urlpatterns = [
    path("users/", UserList.as_view(), name="user-list"),
    path("professionals/", ProfessionlList.as_view(), name="professional-list"),
    path("details_view/<int:pk>/", UsersDetailsView.as_view(), name="user-details"),
    path("booking_list/", BookingView.as_view(), name="booking-view"),
    path("booking_filter/<str:action>/",BookingFilterView.as_view(), name="booking-filter-view"),
    path("booking_details/<int:pk>/",BookingDetails.as_view(), name="booking-details-view"),
    path("payment/",AdminPayment.as_view(), name="payment-details-checkout"),
    path("payment_success/",PaymentSuccessView.as_view() , name='payment-success'),
    path("total/", Total.as_view()),


    # path('sendmail/', send_mail_to_users,name="send_mail_to_users"),
    # path('sendmailattime/', sendmailattime,name="sendmailattime"),


]