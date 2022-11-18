from django.contrib import admin

from .models import Wallet, Transaction, PaymentRequest

admin.site.register(Wallet)
admin.site.register(PaymentRequest)
admin.site.register(Transaction)
