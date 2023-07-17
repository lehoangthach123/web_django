from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms


class WebsiteStateStatusForm(ModelForm):
    # STATUS_CHOICES = [
    #     (False, 'Close'),
    #     (True, 'Open'),
    # ]
    # is_closed = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)

    is_closed = forms.ChoiceField(widget=forms.RadioSelect, choices=((False, 'Open'), (True, 'Close')), label='')


    class Meta:
        model = WebsiteState
        fields = ['is_closed']


class WebsiteStateInformationForm(ModelForm):
    class Meta:
        model = WebsiteState
        fields = ['title','description','keyword']


class ChangeCustomerPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
        strip=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class RegisterCustomerForm(ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['name', 'address', 'mobile', 'email']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Tạo user mới và lưu vào cơ sở dữ liệu
            user = User.objects.create_user(username=username, password=password)

            # Lấy thông tin khách hàng từ cleaned_data
            name = cleaned_data.get('name')
            address = cleaned_data.get('address')
            mobile = cleaned_data.get('mobile')
            email = cleaned_data.get('email')

            # Tạo đối tượng Customer và lưu vào cơ sở dữ liệu
            customer = Customer(user=user, name=name, address=address, mobile=mobile, email=email)
            customer.save()

        return cleaned_data


class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Customer
        fields = ['name', 'address', 'mobile', 'email']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'Enter new password'



class AddAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'descriptions', 'quantity', 'images']


class CategoryInventoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'images']


class Register_User(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(Register_User, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter username....'})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter email....'})
        self.fields['password1'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter password1....'})
        self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter password2....'})

