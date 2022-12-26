from django.db import models
from django.contrib.auth.models import User
import datetime

class Plan(models.Model):
    validity_period = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=100)
    class Meta:
        ordering = ["price"]
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

class Recharge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    recharge_date = models.DateField()
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=True, blank=True)
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    transaction_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    card_holder_name = models.CharField(max_length=100, null=True, blank=True)
    card_expiry = models.CharField(max_length=5, null=True, blank=True)
    card_cvv = models.CharField(max_length=3, null=True, blank=True)
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        if self.transaction_id is None or self.transaction_id == "":
            epoch = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.transaction_id = "TRANSACTION_" + str(self.user.id) + epoch
        super(Transaction, self).save(*args, **kwargs)