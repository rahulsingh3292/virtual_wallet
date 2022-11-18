from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet

from user.models import User
from ..models import Transaction, PaymentRequest, Wallet


@method_decorator(login_required, name="dispatch")
class HomePage(View):
    def get(self, request: HttpRequest):
        balance: int = Wallet.objects.get(user=request.user).balance
        users: "QuerySet[User]" = User.objects.filter(is_superuser=False).exclude(
            id=request.user.id
        )
        return render(request, "home.html", {"users": users, "balance": balance})


@method_decorator(login_required, name="dispatch")
class UserPayOrRequestPage(View):
    def get(self, request: HttpRequest, user_id: int):
        selected_user: User = User.objects.get(id=user_id)
        return render(request, "request_or_pay.html", {"user": selected_user})


@method_decorator(login_required, name="dispatch")
class PaymentsRequestPage(View):
    def get(self, request):
        payment_requests: "QuerySet[PaymentRequest]" = PaymentRequest.objects.filter(
            to_user=request.user
        )
        return render(
            request, "payment_request.html", {"payment_requests": payment_requests}
        )


@method_decorator(login_required, name="dispatch")
class UserTransactionsPage(View):
    def get(self, request: HttpRequest):
        transactions: "QuerySet[Transaction]" = Transaction.objects.filter(
            user=request.user
        )
        return render(request, "transactions.html", {"transactions": transactions})
