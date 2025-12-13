
from django.contrib import admin
from django.urls import path
from BankApp import views
urlpatterns = [
    path('', views.loginPage, name="loginv"),
    path('admin/', admin.site.urls),
    path('home/',views.hompage,name="homev"),
    path('newacc/',views.newAccPage,name="newaccv"),
    path('balance/',views.BalancePage,name='balancev'),
    path('deposit/',views.depositPage,name="depositv"),
    path('withdraw/',views.withdrawPage,name="withdrawv"),
    path('transfer/',views.transferPage,name="transferv"),
    path('close/',views.closePage,name="closev"),
    path('openv/',views.openPage,name="openv"),
    path('manage/',views.managePage,name="managev"),
    path('about/',views.aboutPage,name="aboutv"),
    path('loginv/',views.loginPage,name="loginv"),
    path('empregister/',views.empRegPage,name="empregisterv"),
    path('emploginPage/',views.emploginPage,name="emploginPagev"),
    path('newCustomer/',views.newCustomer,name="newCustomerv"),
    path('customerloginPage/',views.customerloginPage,name="customerloginPagev"),
    path('customerhomePage/',views.customerhomePage,name="customerhomePagev"),
    path('customerbal/',views.customerbalance,name="customerbalv"),
    path('customerdeposit/',views.customerdepositPage,name="customerdepositv"),
    path('customerwithdraw/',views.customerwithdrawPage,name="customerwithdrawv"),
    path('customertransfer/',views.customertransfer,name="customertransferv"),
    path('customerclose/',views.customerclosePage,name="customerclosev")


]
