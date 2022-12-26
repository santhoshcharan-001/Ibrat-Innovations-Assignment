from rest_framework import serializers

from .models import Plan, Recharge

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'validity_period', 'price', 'description')
        read_only_fields = ('id',)

class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = ('id', 'user', 'plan', 'recharge_date')