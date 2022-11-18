from django.db import transaction

from user.models import User
from . import transaction as paymentTransaction
from .models import Wallet


def get_paying_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def get_wallet(user: User) -> Wallet:
    return Wallet.objects.get(user=user)


def get_payment_charges(user: User, amount: int) -> int:
    if user.is_premium_user:
        return int(amount * 0.03)
    else:
        return int(amount * 0.05)


def get_receiving_charges(user: User, amount: int) -> int:
    if user.is_premium_user:
        return int(amount * 0.01)
    else:
        return int(amount * 0.03)


def add_charges_to_admin_account(
    payment_charges: int,
    receiving_charges: int,
    with_user: str,
    to_user: str,
    amount: int,
) -> None:

    user: User = User.objects.get(is_superuser=True)
    wallet: Wallet = get_wallet(user)
    curr_balance: int = wallet.balance

    curr_balance += payment_charges
    paymentTransaction.create_transaction(
        user=user,
        balance=curr_balance,
        amount=payment_charges,
        remark=f"{amount} sent by {with_user} to {to_user}",
    )

    curr_balance += receiving_charges
    paymentTransaction.create_transaction(
        user=user,
        amount=receiving_charges,
        balance=curr_balance,
        remark=f"{amount} received from  {with_user} by {to_user}",
        is_received=True,
    )

    wallet.balance += payment_charges + receiving_charges
    wallet.save()


def have_sufficient_balance_to_pay(
    user: User, wallet_balance: int, amount: int
) -> bool:
    calculated_balance = (wallet_balance) - (
        amount + (int(amount * (0.03 if user.is_premium_user else 0.05)))
    )
    print("total to pay", calculated_balance)
    return calculated_balance >= 0


class Payment:
    def __init__(self, with_user: User, to_user_id: int) -> None:

        self.with_user: User = with_user
        self.paying_user: User = get_paying_user(to_user_id)
        self.payment_detail = {}

    def pay(self, amount: int) -> None:

        paying_user_wallet: Wallet = get_wallet(user=self.paying_user)
        current_user_wallet: Wallet = get_wallet(self.with_user)

        if not have_sufficient_balance_to_pay(
            self.with_user, current_user_wallet.balance, amount
        ):
            detail = {"status": 400, "message": "not enough balance to pay"}
            self.payment_detail = detail
            return

        self.make_payment(current_user_wallet, paying_user_wallet, amount)

    def make_payment(
        self, current_user_wallet: Wallet, paying_user_wallet: Wallet, amount: int
    ) -> None:

        payment_charges: int = get_payment_charges(self.with_user, amount)
        receiving_charges: int = get_receiving_charges(self.paying_user, amount)

        with transaction.atomic():

            current_user_wallet.balance -= amount + payment_charges
            paying_user_wallet.balance += amount - receiving_charges

            paying_user_wallet.save()
            current_user_wallet.save()

            add_charges_to_admin_account(
                payment_charges,
                receiving_charges,
                with_user=self.with_user.username,
                to_user=self.paying_user.username,
                amount=amount,
            )

            paymentTransaction.create_transaction(
                user=self.with_user,
                balance=current_user_wallet.balance,
                amount=amount,
                remark=f"{amount} sent to {self.paying_user.username}",
            )
            paymentTransaction.create_transaction(
                user=self.paying_user,
                amount=amount,
                balance=paying_user_wallet.balance,
                remark=f"{amount} received by {self.with_user.username}",
                is_received=True,
            )

            detail = {"status": 200, "message": "payment done"}
            self.payment_detail = detail
