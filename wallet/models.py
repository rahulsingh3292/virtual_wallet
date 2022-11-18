from django.db import models
from django.conf import settings


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.user.username} ->  {self.balance}"


PAYMENT_REQUEST_STATUS = (
    ("Pending", "Pending"),
    ("Paid", "Paid"),
    ("Rejected", "Rejected"),
)


class PaymentRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_user"
    )
    amount = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=PAYMENT_REQUEST_STATUS, default="Pending"
    )

    def __str__(self):
        return str(self.status)

    @classmethod
    def update_status(cls, id: int, status: str) -> None:
        cls.objects.filter(id=id).update(status=status)
        return


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    charges = models.IntegerField(blank=True)
    balance = models.IntegerField(default=0)
    remark = models.TextField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
