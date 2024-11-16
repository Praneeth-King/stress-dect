from django import forms
from .models import UserRegistrationModel


class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'pattern': '[a-zA-Z ]+',
            'title': 'Please enter only letters',
            'required': 'required'
        }), 
        required=True, 
        error_messages={
            'required': 'Please enter your name',
            'invalid': 'Please enter a valid name (letters only)'
        }
    )
    loginid = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a login ID',
            'pattern': '[a-zA-Z0-9]+',
            'title': 'Please enter letters and numbers only',
            'required': 'required'
        }), 
        required=True,
        error_messages={
            'required': 'Please choose a login ID',
            'invalid': 'Login ID can only contain letters and numbers'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
            'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
            'title': 'Must contain at least one number, uppercase and lowercase letter, and be at least 8 characters long',
            'required': 'required'
        }),
        required=True,
        error_messages={
            'required': 'Please create a password',
            'min_length': 'Password must be at least 8 characters long'
        }
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your mobile number',
            'pattern': '[0-9]{10}',
            'title': 'Please enter a valid 10-digit mobile number',
            'required': 'required'
        }),
        required=True,
        error_messages={
            'required': 'Please enter your mobile number',
            'invalid': 'Please enter a valid 10-digit mobile number'
        }
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required'
        }),
        required=True,
        error_messages={
            'required': 'Please enter your email address',
            'invalid': 'Please enter a valid email address'
        }
    )
    locality = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your locality',
            'required': 'required'
        }),
        required=True,
        error_messages={
            'required': 'Please enter your locality'
        }
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full address',
            'rows': 3,
            'required': 'required'
        }),
        required=True,
        error_messages={
            'required': 'Please enter your address'
        }
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your city',
            'autocomplete': 'off',
            'pattern': '[A-Za-z ]+',
            'title': 'Please enter only letters'
        }), 
        required=True,
        max_length=100
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your state',
            'autocomplete': 'off',
            'pattern': '[A-Za-z ]+',
            'title': 'Please enter only letters'
        }), 
        required=True,
        max_length=100
    )
    status = forms.CharField(
        widget=forms.HiddenInput(), 
        initial='waiting', 
        max_length=100
    )

    class Meta:
        model = UserRegistrationModel
        fields = ['name', 'loginid', 'password', 'mobile', 'email', 'locality', 'address', 'city', 'state', 'status']
