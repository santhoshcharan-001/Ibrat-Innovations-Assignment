from django.urls import path

from .views import GetPlanDetails,GetRechargePlanDetails
from .views import Payment,CompletePayment

urlpatterns = [
    path('plans/', GetPlanDetails.as_view()),
    path('getrechargeplandetails/', GetRechargePlanDetails.as_view()),
    path('payment/', Payment.as_view()),
    path('completepayment/', CompletePayment.as_view()),
]