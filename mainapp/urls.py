from django.urls import path

from .views import *


urlpatterns = [
   
    path("dashboard/",dashboard, name="dashboard"),
    path("member-profile/",member_profile, name="member_profile"),
    path("next-of-kinn/",next_of_kinn, name="nextofkinn"),
    path("next-of-kinn-list/",next_of_kinn_list, name="nextofkinnlist"),
    path("subscriptions/",subscriptions, name="subscriptions"),
    path("subscriptions-list/",subscriptions_list, name="subscriptionslist"),
    path("nominees/",nominees, name="nominees"),
    path("nominee-list/",nominees_list, name="nomineelist"),
    path('get-tenure-details/<str:loantype_id>/',get_tenure_details,name='get_tenure_details'),
    path("",login, name=""),
    path("login",login, name="login"),
    path("register/",register, name="register"),
    path("verify/",verify, name="verify"),
    path("basic/",basic, name="basic"),
    path("download/",download, name="download"),
    path("loanapplication/",loanapplication, name="loanapplication"),
    path("loan-calculator/",loancalculator, name="loancalculator"),
    path("applyloan/",applyloan, name="applyloan"),
    path("basic1/",basic1, name="basic1"),
    path("repayment-Schedule/",repayment_Schedule, name="repayment_Schedule"),
    path("req/",req, name="req"),
    path("deposit/",deposit, name="deposit"),
    path("account/",account, name="account"),
    path("account-list/",account_list, name="account_list"),
    path("accounttransfer/",accounttransfer, name="accounttransfer"),
    path("bank/",bank, name="bank"),
    path("edit_req/",edit_req, name="edit_req"),
    path('payment_process/<str:schedule_id>/<str:loan_application_id>/',payment_process,name='payment_process'),


]