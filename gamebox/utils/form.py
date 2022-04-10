from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from gamebox import models
from gamebox.utils.bootstrap import BootStrapModelForm
from gamebox.utils.encrypt import md5
from gamebox.views.cart import getUser


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        max_length=16,
        min_length=3,
        required=True,
        label="用户名",
        help_text='3-15 characters！',
        validators=[RegexValidator(r'^(\w)+$', 'can only contains letter, number and _！')],
        error_messages={
            'required': 'username can not be null',
            'min_length': 'at least 3 characters',
            'max_length': 'username less than 16 characters',
            'invalid': 'invalid'
        })
    password = forms.CharField(
        label="Password",
        validators=[RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')],
        widget=forms.PasswordInput,
        error_messages={
            'invalid': 'more thant 8 chars and contain at least 1 letter and 1 number'
        })

    age = forms.IntegerField(
        label="age",
        min_value=0
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "gender"]


class QueryModelForm(BootStrapModelForm):
    class Meta:
        model = models.Appeal
        fields = ["title", "issue"]

# class NumberModelForm(BootStrapModelForm):
#     mobile = forms.CharField(
#         label="mobile number",
#         validators=[RegexValidator(r'^1[3-9]\d{9}$', 'wrong form')]
#     )
#
#     class Meta:
#         model = models.PrettyNum
#         fields = ['mobile', 'price', 'level', 'status']
#
#
# class NumberEditModelForm(BootStrapModelForm):
#     # mobile = forms.CharField(
#     #     disabled=True
#     # )
#
#     class Meta:
#         model = models.PrettyNum
#         fields = ['mobile', 'price', 'level', 'status']
#
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#
#         exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
#         if exists:
#             raise ValidationError("PhoneNumberAlreadyExists")
#
#         return txt_mobile
#
#
# class NumberModelForm(BootStrapModelForm):
#     mobile = forms.CharField(
#         label="mobile number",
#         validators=[RegexValidator(r'^1[3-9]\d{9}$', 'wrong form')]
#     )
#
#     class Meta:
#         model = models.PrettyNum
#         fields = ['mobile', 'price', 'level', 'status']
