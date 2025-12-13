from django.shortcuts import render,redirect
from django.db import transaction
from django.contrib import messages
from BankApp.models import newReg
from BankApp.models import empReg
from BankApp.forms import AccForm
from BankApp.forms import balanceForm
from BankApp.forms import depositForm
from BankApp.forms import withdrawForm
from BankApp.forms import transferForm
from BankApp.forms import closeForm
from BankApp.forms import openForm
from BankApp.forms import empLoginForm
from BankApp.forms import empRegForm
from BankApp.forms import customerLogin
from BankApp.forms import customerBal
from BankApp.forms import customerdeposit
from BankApp.forms import customerwithdraw
from BankApp.forms import customertransferForm
from BankApp.forms import customercloseForm

# Create your views here.
def hompage(request):
    return render(request,"home.html")

# Creating Account
def newAccPage(request):
    form=AccForm()
    if request.method == "POST":
        form=AccForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            messages.success(request,"Congratulations!...You have Created Account in LBI")
            return render(request,"accreg.html",{"form":form})
            
        else:
            messages.error(request,"Error in Creating your Account!!!")
            return render(request,"accreg.html",{"form":form})
    else:
        form=AccForm()
    return render(request,"accreg.html",{"form":form})

# Fetching Balance
def BalancePage(request):
    form = balanceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            account_number = int(form.cleaned_data['account_number'])
            password = form.cleaned_data['password']
            try:
                user = newReg.objects.get(account_number=account_number, password=password)
                if not user.active:
                    messages.error(request,"Account is Deactivated....You can't check your Balance")
                    return render(request, "balance.html", {"form": form})
                else:
                    bal = user.amount
                    name=user.name
                    mobile=user.mobile_no
                    acc=user.account_number
                    return render(request, "showbalance.html", {"bal": bal, "account_number": account_number,"name":name,"mobile":mobile,"acc":acc})
            except newReg.DoesNotExist:
                messages.error(request, "Invalid Account Number or Password")
    return render(request, "balance.html", {"form": form})

#Deposit Amount
def depositPage(request):
    form=depositForm()
    if request.method=="POST":
        form=depositForm(request.POST)
        if form.is_valid():
            account_number=int(form.cleaned_data['account_number'])
            password=form.cleaned_data['password']
            amount=form.cleaned_data['amount']
            try:
                user=newReg.objects.get(account_number=account_number, password=password)
                if not user.active:
                    messages.error(request,"Account is Deactivated....You can't Deposit amount")
                    return render(request, "deposit.html", {"form": form})
                else:
                    name=user.name
                    old_bal=user.amount
                    new_amount=old_bal+amount
                    user.amount=new_amount
                    user.save()
                    return render(request,"depositout.html",{"name":name,"old_bal":old_bal,"amount":amount,"new_amount":new_amount})
            except newReg.DoesNotExist:
                messages.error(request,"Invalid Account Number or Password")
    return render(request,"deposit.html",{"form":form})

#WIthdrawl
def withdrawPage(request):
    form=withdrawForm()
    if request.method=="POST":
        form=withdrawForm(request.POST)
        if form.is_valid():
            account_number=int(form.cleaned_data['account_number'])
            password=form.cleaned_data['password']
            amount=float(form.cleaned_data['amount'])
            try:
                user=newReg.objects.get(account_number=account_number, password=password)
                if not user.active:
                    messages.error(request,"Account is Deactivated....You can't Withdraw Money")
                    return render(request, "withdraw.html", {"form": form})
                else:
                    name=user.name
                    old_bal=user.amount
                    if old_bal>=amount:
                        new_amount=old_bal-amount
                        user.amount=new_amount
                        user.save()
                        return render(request,"withdrawout.html",{"name":name,"old_bal":old_bal,"new_amount":new_amount,"amount":amount})
                    else:
                        messages.error(request,"Insuficient Funds in your Account")
                        return render(request,"withdraw.html",{"name":name,"form":form})
            except newReg.DoesNotExist:
                messages.error(request,"Invalid Account Number or Password")
    return render(request,"withdraw.html",{"form":form})


#Transfer Money
def transferPage(request):
    form=transferForm()
    if request.method == "POST":
        form=transferForm(request.POST)
        if form.is_valid():
            account_number=int(form.cleaned_data['account_number'])
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            target_account=int(form.cleaned_data['target_account'])
            amount=float(form.cleaned_data['amount'])
            try:
                user1=newReg.objects.get(account_number=account_number,password=password,name=name)
                user2=newReg.objects.get(account_number=target_account)
                if not (user1.active and user2.active):
                    messages.error(request,"One of the Accounts is Deactivated....You can't Transfer Money")
                    return render(request, "transfer.html", {"form": form})
                else:
                    name2=user2.name
                    old_bal1=user1.amount
                    old_bal2=user2.amount
                    if old_bal1>=amount:
                        new_bal1=old_bal1-amount
                        new_bal2=old_bal2+amount
                        user1.amount=new_bal1
                        user2.amount=new_bal2
                        user1.save()
                        user2.save()
                        return render(request,"transferout.html",{"name2":name2,"name":name,"old_bal1":old_bal1,"amount":amount,"new_bal1":new_bal1,"old_bal2":old_bal2,"new_bal2":new_bal2})
                    else:
                        messages.error(request,"Insuficient Funds in your Account")
                        return render(request,"transfer.html",{"name":name,"form":form})
            except newReg.DoesNotExist:
                messages.error(request,"Invalid Account Number or Password")
    return render(request,"transfer.html",{"form":form})

#Close Account
def closePage(request):
    form=closeForm()
    if request.method == "POST":
        form=closeForm(request.POST)
        if form.is_valid():
            account_number=int(form.cleaned_data['account_number'])
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            try:
                user=newReg.objects.get(account_number=account_number,name=name,password=password)
                if not user.active:
                    messages.error(request,"Account is already Deactivated....")
                    return render(request, "close.html", {"form": form})
                user.active=False
                user.save()
                messages.success(request,"Account Deactivated Successfully")
                return render(request,"closeout.html",{"name":name,"account_number":account_number})
            except newReg.DoesNotExist:
                messages.error(request,"Invalid Account Number or Password")
    return render(request,"close.html",{"form":form})

#open account
def openPage(request):
    form=openForm()
    if request.method == "POST":
        form = openForm(request.POST)
        if form.is_valid():
            account_number=int(form.cleaned_data['account_number'])
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            try:
                user=newReg.objects.get(account_number=account_number,name=name,password=password)
                if not user.active:
                    user.active=True
                    user.save()
                    messages.success(request,"Account Activated Successfully...!")
                    return render(request,"openout.html",{"name":name,"account_number":account_number})
                else:
                    messages.error(request,"Account is already in Active Status...")
                    return render(request,"open.html",{"form":form})
            except newReg.DoesNotExist:
                messages.error(request,"Inavild Account Details")
    return render(request,"open.html",{"form":form})

def managePage(request):
    return render(request,"manage.html")

def aboutPage(request):
    return render(request,"about.html")

def loginPage(request):
    return render(request,"loginpage.html")
#-----------------------------------------
#employee Registration
def empRegPage(request):
    form=empRegForm()
    if request.method == "POST":
        form=empRegForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            messages.success(request,"Congratulations!...Please Sign IN")
            return render(request,"empreg.html",{"form":form})    
        else:
            messages.error(request,"Error while Registering")
            return render(request,"empreg.html",{"form":form})
    else:
        form=empRegForm()
    return render(request,"empreg.html",{"form":form})

#employee login
def emploginPage(request):
    form=empLoginForm()
    if request.method=="POST":
        form=empLoginForm(request.POST)
        if form.is_valid():
            empid=form.cleaned_data['empid']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            try:
                user=empReg.objects.get(empid=empid,email=email,password=password)
                return render(request,"home.html")
            except empReg.DoesNotExist:
                messages.error(request,"Invalid details")
                return render(request,"emplogin.html",{"form":form})
    return render(request,"emplogin.html",{"form":form})

#----------------Customer----------------------
def newCustomer(request):
    form=AccForm()
    if request.method == "POST":
        form=AccForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            messages.success(request,"Congratulations!...You have Created Account in LBI")
            return render(request,"customerreg.html",{"form":form})
        else:
            messages.error(request,"Error in Creating your Account!!!")
            return render(request,"customerreg.html",{"form":form})
    else:
        form=AccForm()
    return render(request,"customerreg.html",{"form":form})


def customerloginPage(request):
    form=customerLogin()
    if request.method=="POST":
        form=customerLogin(request.POST)
        if form.is_valid():
            account_number=int(form.cleaned_data['account_number'])
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            try:
                user=newReg.objects.get(account_number=account_number,name=name,password=password)
                if not user.active:
                    messages.error(request,"Account is Deactivated....You can't Login")
                    return render(request, "customerlogin.html", {"form": form})
                else:
                    request.session['customer_acc'] = user.account_number
                    request.session['customer_name'] = user.name
                    request.session['customer_mobile'] = user.mobile_no
                    name=user.name
                    acc=user.account_number
                    mobile=user.mobile_no
                    return render(request,"customerhome.html",{"name":name,"acc":acc,"mobile":mobile})
            except newReg.DoesNotExist:
                messages.error(request,"Invalid Customer Details")
                return render(request,"customerlogin.html",{"form":form})
        else:
            form=customerLogin()
    return render(request,"customerlogin.html",{"form":form})

def customerhomePage(request):
    acc = request.session.get('customer_acc')
    name=request.session.get('customer_name')
    mobile=request.session.get('customer_mobile')
    return render(request,"customerhome.html",{"acc":acc,"name":name,"mobile":mobile})

def customerbalance(request):
    acc = request.session.get('customer_acc')
    name=request.session.get('customer_name')
    form=customerBal()
    if request.method =="POST":
        form=customerBal(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            try:
                user=newReg.objects.get(account_number=acc)
                if user.password==password:
                    return render(request,"custbalout.html",{"form":form,"name":user.name,"acc":user.account_number,"balance":user.amount})
                else:
                    messages.error(request,"Invalid Password")
                    return render(request,"customerbal.html",{"form":form,"name":name,"acc":acc})
            except newReg.DoesNotExist:
                messages.error(request,"User Does not Exist")
                return render(request,"customerbal.html",{"form":form})
        else:
            form=customerBal()
    return render(request,"customerbal.html",{"form":form,"acc":acc,"name":name})


def customerdepositPage(request):
    acc=request.session.get('customer_acc')
    name=request.session.get('customer_name')
    form=customerdeposit()
    if request.method == "POST":
        form=customerdeposit(request.POST)
        if form.is_valid():
            amount=float(form.cleaned_data['amount'])
            password=form.cleaned_data['password']
            try:
                user = newReg.objects.get(account_number=acc)
                if user.password==password:
                    old_bal=user.amount
                    new_bal=old_bal+amount
                    user.amount=new_bal
                    user.save()
                    return render(request,"custdepout.html",{"name":name,"acc":user.account_number,"old_bal":old_bal,"amount":amount,"new_bal":new_bal})
                else:
                    messages.error(request,"Invalid Password")
                    return render(request,"customerdeposit.html",{"form":form,"name":name,"acc":acc})
            except newReg.DoesNotExist:
                return render(request,"customerdeposit.html",{"form":form})
        else:
            form=customerdeposit()
    return render(request,"customerdeposit.html",{"form":form,"name":name,"acc":acc})

def customerwithdrawPage(request):
    acc=request.session.get('customer_acc')
    name=request.session.get('customer_name')
    form=customerwithdraw()
    if request.method == "POST":
        form=customerwithdraw(request.POST)
        if form.is_valid():
            amount=float(form.cleaned_data['amount'])
            password=form.cleaned_data['password']
            try:
                user = newReg.objects.get(account_number=acc)
                if user.password==password:
                    if user.amount>=amount:
                        old_bal=user.amount
                        new_bal=old_bal-amount
                        user.amount=new_bal
                        user.save()
                        return render(request,"custwithout.html",{"name":name,"acc":user.account_number,"old_bal":old_bal,"amount":amount,"new_bal":new_bal})
                    else:
                        messages.error(request,"Insufficient Funds")
                        return render(request,"customertransfer.html",{"form":form,"name":name,"acc":acc})
                else:
                    messages.error(request,"Invalid Password")
                    return render(request,"customerwithdraw.html",{"form":form,"name":name,"acc":acc})
            except newReg.DoesNotExist:
                return render(request,"customerwithdraw.html",{"form":form})
        else:
            form=customerdeposit()
    return render(request,"customerwithdraw.html",{"form":form,"name":name,"acc":acc})

def customertransfer(request):
    acc=request.session.get('customer_acc')
    name=request.session.get('customer_name')
    form=customertransferForm()
    if request.method=="POST":
        form=customertransferForm(request.POST)
        if form.is_valid():
            target_account=form.cleaned_data['target_account']
            amount=float(form.cleaned_data['amount'])
            password=form.cleaned_data['password']
            try:
                user1=newReg.objects.get(account_number=acc)
                user2=newReg.objects.get(account_number=target_account)
                if not user2.active:
                    messages.error(request,"Target Account is Deactivated")
                    return render(request,"customertransfer.html",{"form":form,"name":name,"acc":acc})
                elif user1.password==password:
                    if user1.amount>=amount:
                        old_bal1=user1.amount
                        new_bal1=old_bal1-amount
                        old_bal2=user2.amount
                        new_bal2=old_bal2+amount
                        user1.amount=new_bal1
                        user2.amount=new_bal2
                        user1.save()
                        user2.save()
                        return render(request,"custtransferout.html",{"name":name,"acc":acc,"old_bal1":old_bal1,"amount":amount,"new_bal1":new_bal1,"name2":user2.name})
                    else:
                        messages.error(request,"Insufficient Funds")
                        return render(request,"customertransfer.html",{"form":form,"name":name,"acc":acc})
                else:
                    messages.error(request,"Check the Details Entered")
                    return render(request,"customertransfer.html",{"form":form,"name":name,"acc":acc})
            except newReg.DoesNotExist:
                return render(request,"customertransfer.html",{"form":form})
        else:
            form=customertransferForm()
    return render(request,"customertransfer.html",{"form":form,"name":name,"acc":acc})

def customerclosePage(request):
    acc=request.session.get('customer_acc')
    name=request.session.get('customer_name')
    form=customercloseForm()
    if request.method=="POST":
        form=customercloseForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            try:
                user=newReg.objects.get(account_number=acc)
                if user.password==password:
                    user.active=False
                    user.save()
                    return render(request,"loginpage.html")
                else:
                    messages.error(request,"Invalid Password")
                    return render(request,"customerclose.html",{"form":form,"name":name,"acc":acc})
            except newReg.DoesNotExist:
                return render(request,"customerclose.html",{"form":form,"name":name,"acc":acc})
        else:
            form=customercloseForm()
    return render(request,"customerclose.html",{"form":form,"name":name,"acc":acc})