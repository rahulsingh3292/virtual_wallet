from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from ..payment import Payment
from ..models import PaymentRequest


class BasePayView(View):
    def pay(self, user: User, data: dict[str, any]) -> dict[str, any]:
        amount: int = int(data.get("amount"))
        to_user_id: int = data.get("to_user_id")
        payment: Payment = Payment(with_user=user, to_user_id=to_user_id)
        payment.pay(amount)
        return payment.payment_detail


@method_decorator(csrf_exempt, name="dispatch")
class PayPayment(BasePayView, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            payment_detail: dict[str, any] = self.pay(request.user, request.POST)
            return JsonResponse(payment_detail)
        except Exception as DBError:
            print(DBError)
            return JsonResponse({"status": 503, "message": "error from database"})


@method_decorator(csrf_exempt, name="dispatch")
class RequestPayment(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data: dict[str, any] = request.POST
        to_user: User = User.objects.get(id=data.get("to_user_id"))

        try:
            PaymentRequest.objects.create(
                from_user=request.user, to_user=to_user, amount=data.get("amount")
            )
            return JsonResponse({"status": 200, "message": "payment request sent"})

        except Exception as UserNotFound:
            return JsonResponse({"status": 404, "message": "user not found"})


@method_decorator(csrf_exempt, name="dispatch")
class AcceptOrDenyPaymentRequest(BasePayView):
    def post(self, request: HttpRequest) -> JsonResponse:
        data: dict[str, any] = request.POST.dict()
        action: str = data.pop("action")
        payment_request_id: int = data.pop("payment_request_id")

        if action == "pay":
            try:
                payment_detail: dict[str, any] = self.pay(request.user, data)

                if payment_detail["status"] == 200:
                    PaymentRequest.update_status(payment_request_id, "Paid")
                    payment_detail.update({"action": "paid"})
                return JsonResponse(payment_detail)

            except Exception as Error:
                return JsonResponse({"status": 503, "message": "server error"})

        PaymentRequest.update_status(payment_request_id, "Rejected")
        return JsonResponse({"status": 200, "action": "reject"})
