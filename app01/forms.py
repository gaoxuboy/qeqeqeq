from django import forms
from django.core.exceptions import ValidationError


class Form(forms.Form):
    username = forms.CharField(

        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '长度大于3小于8，字母或数字'}
                               ))
    password = forms.CharField(min_length=3, max_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '长度大于3小于8'}))
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '长度大于3小于8'}))

    # phone_number = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '长度为11位'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))

    verification = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'verfication'}))

    def __init__(self,request,*args,**kwargs):
        super(Form,self).__init__(*args,**kwargs)
        self.request=request

    def clean_verification(self):
        if self.cleaned_data['verification'].upper() == self.request.session["valid_code"].upper() :
            return self.cleaned_data['verification']
        else:
            raise ValidationError('验证输入不一致')

    def clean_username(self):
        if self.cleaned_data["username"].isdigit() or self.cleaned_data["username"].isalpha():
            return self.cleaned_data['username']
        else:

             raise ValidationError('用户名输入错误')

    def clean_password(self):
        if len(self.cleaned_data["password"]) > 3 and len(self.cleaned_data["password"]) < 8:
            return self.cleaned_data['password']
        else:
            raise ValidationError('密码输入错误')
    #
    # def clean_phone_number(self):
    #     if len(self.cleaned_data.get('phone_number')) != 11:
    #         raise ValidationError('手机号错误')
    #     else:
    #         return self.cleaned_data['phone_number']

    def clean(self):

        if self.cleaned_data.get('password',None) and self.cleaned_data.get("new_password",None):
            if self.cleaned_data['password'] == self.cleaned_data['new_password']:
                return self.cleaned_data
            else:
                raise ValidationError('密码不一致')

class Comment(forms.Form):
    username=forms.CharField()
    comment=forms.CharField()