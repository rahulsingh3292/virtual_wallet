from django.dispatch import receiver
from django.db.models.signals import post_save

from wallet.models import Wallet
from .models import User

PREMIUM_USER_BALANCE: int = 2500
NON_PREMIUM_USER_BALANCE: int = 1000


@receiver(post_save, sender=User)
def create_user_wallet_account(sender, instance, created, **kwargs) -> None:
    if created:

        user_wallet: Wallet = Wallet(user=instance)

        if instance.is_superuser:
            user_wallet.balance = 0
            user_wallet.save()
            return

        if instance.is_premium_user:
            user_wallet.balance = PREMIUM_USER_BALANCE
        else:
            user_wallet.balance = NON_PREMIUM_USER_BALANCE

        user_wallet.save()
