from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import PasswordReset
from salaoecia.core.utils import generate_hash_key
from salaoecia.core.mail import send_mail_template
import salaoecia.utils.utils

User = get_user_model()


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário encontrado com este e-mail.')

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha'
        context = {
            'reset': reset
        }
        send_mail_template(subject, template_name, context, [user.email])


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(forms.ModelForm):
    name = forms.CharField(label='Nome Completo')
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    birth = forms.DateField(label='Data de nascimento', widget=DateInput)
    address = forms.CharField(label='Endereço')
    number = forms.CharField(label='Número')
    complement = forms.CharField(label='Complemento')
    neighborhood = forms.CharField(label='Bairro')
    zip_code = forms.CharField(label='CEP')
    city = forms.CharField(label='Cidade')
    #fx_salario = forms.CharField(label='Fx')
    #state = forms.ChoiceField(label='Estado')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha não esta correta.')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.name = self.cleaned_data.get("name")
        user.set_password(self.data['password1'])
        user.birth = self.cleaned_data.get("birth")
        user.address = self.cleaned_data.get("address")
        user.number = self.cleaned_data.get("number")
        user.complement = self.cleaned_data.get("complement")
        user.neighborhood = self.cleaned_data.get("neighborhood")
        user.zip_code = self.cleaned_data.get("zip_code")
        user.city = self.cleaned_data.get("city")
        #user.state = self.cleaned_data.get("state")

        if commit:
            user.save()
        return user,

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'birth', 'address', 'number', 'complement', 'neighborhood', 'zip_code', 'city', 'fx_salario', 'state']


class EditAccountForm(forms.ModelForm):
    name = forms.CharField(label='Nome Completo')
    birth = forms.DateField(label='Data de nascimento', widget=DateInput)
    address = forms.CharField(label='Endereço')
    number = forms.CharField(label='Número')
    complement = forms.CharField(label='Complemento')
    neighborhood = forms.CharField(label='Bairro')
    zip_code = forms.CharField(label='CEP')
    city = forms.CharField(label='Cidade')
    #fx_salario = forms.ChoiceField(label='Fx')

    class Meta:
        model = User
        fields = ['name', 'birth', 'email', 'name', 'address', 'number', 'complement', 'neighborhood', 'zip_code', 'city', 'fx_salario', 'state']

