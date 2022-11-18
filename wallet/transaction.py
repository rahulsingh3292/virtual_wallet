from user.models import User
from .models import Transaction

PAYMENT_SEND_PREMIUM_USER_CHARGES: int = 3
PAYMENT_SEND_NON_PREMIUM_USER_CHARGES: int = 5
PAYMENT_RECEIVE_PREMIUM_USER_CHARGES: int = 1
PAYMENT_RECEIVE_NON_PREMIUM_USER_CHARGES: int = 3


def get_charges(user: User, is_received: bool = False) -> int:
    if user.is_superuser:
        return 0

    elif user.is_premium_user and not is_received:
        return PAYMENT_SEND_PREMIUM_USER_CHARGES
    elif not user.is_premium_user and not is_received:
        return PAYMENT_SEND_NON_PREMIUM_USER_CHARGES

    elif user.is_premium_user:
        return PAYMENT_RECEIVE_PREMIUM_USER_CHARGES
    else:
        return PAYMENT_RECEIVE_NON_PREMIUM_USER_CHARGES


def create_transaction(
    user: User, amount: int, balance: int, remark: str, is_received: bool = False
) -> None:
    transaction = Transaction(user=user, amount=amount, balance=balance, remark=remark)

    if not is_received:
        if not user.is_superuser:
            transaction.is_sent = True

    transaction.charges = get_charges(user, is_received)
    transaction.save()
