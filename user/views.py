from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password

from .models import User


@method_decorator(csrf_exempt, name="dispatch")
class SignUpView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "signup.html")

    def post(self, request: HttpRequest) -> JsonResponse:
        username: str = request.POST.get("username")

        if User.is_user_exist(username):
            return JsonResponse({"status": 403})

        data: dict[str, any] = request.POST.dict()
        data["is_premium_user"] = (
            True if data["is_premium_user"].lower() == "yes" else False
        )
        data["password"] = make_password(data["password"])
        User.objects.create(**data)
        return JsonResponse({"status": 201})


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html")

    def post(self, request: HttpRequest) -> JsonResponse:
        user = authenticate(request, **request.POST.dict())
        if user is not None:
            login(request, user)
            return JsonResponse({"status": 200})
        return JsonResponse({"status": 404})


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("/accounts/login/")
