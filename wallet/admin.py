from django.contrib import admin

from .models import Wallet, Transaction, WalletAddress, CompanyWallet, UserWallet


admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(WalletAddress)
admin.site.register(CompanyWallet)
admin.site.register(UserWallet)

