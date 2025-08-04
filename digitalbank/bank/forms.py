from django import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount to Deposit',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount to Withdraw',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalpha():
            raise forms.ValidationError("Username should contain only letters.")
        return username.capitalize()

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[\W_]', password):
            raise forms.ValidationError("Password must include at least one special character.")
        return password

# transfer
class TransferForm(forms.Form):  # ✅ यही नया जोड़ना है
    recipient = forms.CharField(label="Recipient Username")
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2)
# update profile forms
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        
        }    