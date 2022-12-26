from django.shortcuts import render
from .models import Plan, Recharge, Transaction
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializers import PlanSerializer, RechargeSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class GetPlanDetails(APIView):
    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRechargePlanDetails(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # user = User.objects.get(id=1)
        user = request.user
        recharge = Recharge.objects.filter(user=user)
        serializer = RechargeSerializer(recharge, many=True)
        return Response(serializer.data)

class Payment(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            user = request.user
            plan_id = request.data['plan_id']
            plan = Plan.objects.get(id=plan_id)
            card_number = request.data['card_number']
            card_holder_name = request.data['card_holder_name']
            card_expiry = request.data['card_expiry']
            card_cvv = request.data['card_cvv']
            transaction = Transaction(user=user, plan=plan, transaction_date=datetime.now(), card_number=card_number, 
                            card_holder_name=card_holder_name, card_expiry=card_expiry, 
                            card_cvv=card_cvv, is_completed=False)
            transaction.save()
            return Response({"message": "Payment Successful","transaction_id":transaction.id}, 
                                status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"message": "Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)


class CompletePayment(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            user = request.user
            transaction_id = request.data['transaction_id']
            transaction = Transaction.objects.get(id=transaction_id)
            otp = request.data['otp']
            if otp == transaction.otp == "123456":
                transaction.is_completed = True
                transaction.save()
                r = Recharge.objects.filter(user=user).order_by('-recharge_date').first()
                if r:
                    if datetime.now() >= r.recharge_date + r.plan.validity_period:
                        recharge = Recharge(user=user, plan=transaction.plan, 
                                            recharge_date=datetime.now(), 
                                            transaction=transaction,subscription_start_date=datetime.now(), 
                                            subscription_end_date=datetime.now() + transaction.plan.validity_period)
                        recharge.save()
                    else:
                        recharge = Recharge(user=user, plan=transaction.plan, 
                                        recharge_date=datetime.now(), transaction=transaction,
                                        subscription_start_date=r.subscription_end_date, 
                                        subscription_end_date=r.subscription_end_date + transaction.plan.validity_period)
                        recharge.save()
                else:
                    recharge = Recharge(user=user, plan=transaction.plan, recharge_date=datetime.now(), 
                                    transaction=transaction,subscription_start_date=datetime.now(), 
                                    subscription_end_date=datetime.now() + transaction.plan.validity_period)
                    recharge.save()
                return Response({"message": "Payment Successful"}, status=status.HTTP_201_CREATED)
            else:
                transaction_id = request.data['transaction_id']
                transaction = Transaction.objects.get(id=transaction_id)
                # delete transaction
                transaction.delete()
                return Response({"message": "Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)