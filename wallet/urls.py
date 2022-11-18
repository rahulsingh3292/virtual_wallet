from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view()),
    path("user/<int:user_id>/", views.UserPayOrRequestPage.as_view()),
    path("user/transactions/", views.UserTransactionsPage.as_view()),
    path("user/payment_requests/", views.PaymentsRequestPage.as_view()),
    path("payment/request/", views.RequestPayment.as_view()),
    path("payment/pay/", views.PayPayment.as_view()),
    path("payment_request/pay_or_reject/", views.AcceptOrDenyPaymentRequest.as_view()),
]
