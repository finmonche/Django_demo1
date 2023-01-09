from django import forms

class LeginForm(forms.Form):
    userid = forms.CharField(label='客戶帳號', required=True)
    password = forms.CharField(label='客戶密碼', widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    userid = forms.CharField(label='客戶帳號', required=True)
    name = forms.CharField(label='客戶姓名', required=True)
    password = forms.CharField(label='客戶密碼', widget=forms.PasswordInput)
    password1 = forms.CharField(label='確認密碼', widget=forms.PasswordInput)
    birthday = forms.DateField(label='出生日期' , error_messages={'invalid':'無效的日期'})
    address= forms.CharField(label='通訊地址', required=False)
    phone = forms.CharField(label='電話號碼', required=False)
    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError('兩次密碼不同')
        return password1