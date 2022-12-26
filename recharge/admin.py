from django.contrib import admin

# Register your models here.
from .models import Plan, Recharge, Transaction

admin.site.register(Plan)
# admin.site.register(UserProfile)
admin.site.register(Recharge)
admin.site.register(Transaction)
