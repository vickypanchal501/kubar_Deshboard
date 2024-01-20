# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserPersonalDetails

# class NoSpaceValidator:
#     def __call__(self, value):
#         if ' ' in value:
#             raise ValidationError(
#                 _("Username cannot contain spaces."),
#                 code='invalid_username',
#             )

class SignUpForm(UserCreationForm):
    # username = forms.CharField(validators=[NoSpaceValidator()])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'number','password1']
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))
#     class Meta:
#         model = OTPDevice
    
class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = UserPersonalDetails
        fields = ['pan_number', 'aadhar_number']        