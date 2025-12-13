from django import forms
from BankApp.models import newReg
from BankApp.models import empReg

class AccForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput,max_length=10)
    class Meta:
        model=newReg
        fields=['account_number','name','amount','mobile_no','address','password']
        widgets={"password":forms.PasswordInput(),"address":forms.Textarea()}

    #verfying password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
#Employee
class empRegForm(forms.ModelForm):
    class Meta:
        model=empReg
        fields=['empid','name','mobile','email','password']
        widgets={"password":forms.PasswordInput()}

class empLoginForm(forms.Form):
    empid=forms.IntegerField()
    email=forms.EmailField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput,max_length=10)


    
class balanceForm(forms.Form):
    account_number=forms.CharField(widget=forms.NumberInput,max_length=20)
    password=forms.CharField(widget=forms.PasswordInput)

class depositForm(forms.Form):
    account_number=forms.CharField(widget=forms.NumberInput,max_length=20)
    password=forms.CharField(widget=forms.PasswordInput,max_length=10)
    amount=forms.FloatField()

class withdrawForm(forms.Form):
    account_number=forms.CharField(max_length=20,widget=forms.NumberInput)
    password=forms.CharField(widget=forms.PasswordInput,max_length=10)
    amount=forms.FloatField()

class transferForm(forms.Form):
    account_number=forms.CharField(max_length=20,widget=forms.NumberInput)
    name=forms.CharField(max_length=30)
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)
    target_account=forms.CharField(max_length=20,widget=forms.NumberInput)
    amount=forms.FloatField()

class closeForm(forms.Form):
    account_number=forms.CharField(max_length=20,widget=forms.NumberInput)
    name=forms.CharField(max_length=30)
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)  

class openForm(forms.Form):
    account_number=forms.CharField(max_length=20,widget=forms.NumberInput)
    name=forms.CharField(max_length=30)
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)
        

#---------------------Customer--------------------------------
class customerLogin(forms.Form):
    account_number=forms.CharField(max_length=20,widget=forms.NumberInput)
    name=forms.CharField(max_length=30)
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)

class customerBal(forms.Form):
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)

class customerdeposit(forms.Form):
    amount=forms.FloatField()
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)

class customerwithdraw(forms.Form):
    amount=forms.FloatField()
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)

class customertransferForm(forms.Form):
    target_account=forms.CharField(max_length=20,widget=forms.NumberInput)
    amount=forms.FloatField()
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)

class customercloseForm(forms.Form):
    password=forms.CharField(max_length=10,widget=forms.PasswordInput)