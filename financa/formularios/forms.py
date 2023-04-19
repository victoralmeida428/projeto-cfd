from django import forms
from financa.models import BancoUsuarios
from django.contrib.auth.models import User


class RegistroSite(forms.Form):
    nome = forms.CharField(max_length=50, required=True,
                           label='Nome Completo', 
                           widget=forms.TextInput(attrs={'placeholder': 'Nome Completo'}))
    email = forms.EmailField(label='E-mail', required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'email@dominio.com'}))
    login = forms.CharField(max_length=15, required=True, label='Login',
                            widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    senha = forms.CharField(required=True, widget=forms.PasswordInput())
    senha_rep = forms.CharField(required=True,
                                widget=forms.PasswordInput(),
                                label='Repetir Senha')
    salario = forms.DecimalField(required=True, max_digits=100, label='Salário (R$):',
                                 widget=forms.NumberInput(attrs={'placeholder': '6000.00'}))
    nascimento = forms.DateField(required=True,
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    
    def clean_senha_rep(self):
        senha1 = self.cleaned_data.get('senha')
        senha2 = self.cleaned_data['senha_rep']
        if senha2:
            if senha1 != senha2:
                raise forms.ValidationError('Senhas não coincidem')
    
    def clean_login(self):
        login = self.cleaned_data.get('login')
        login = login.strip()
        banco = User.objects.filter(username=login).values()
        if len(banco) != 0:
            raise forms.ValidationError("Login já existe")
        
        if ' ' in login:
            raise forms.ValidationError("O Login não pode conter espaço")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        banco = User.objects.filter(email=email).values()
        if len(banco) != 0:
            raise forms.ValidationError("Este e-mail já foi cadastrado")


class Login(forms.Form):
    login = forms.CharField(max_length=15, required=True, label='Login',
                            widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'password'}))

    def clean_password(self):
        senha = self.cleaned_data.get('password')
        login = self.cleaned_data.get('login')
        banco = BancoUsuarios.objects.filter(login=login).values()
        if len(banco) == 0:
            print('nao existe')
            raise forms.ValidationError('Usuário não existe')
        if banco[0]['senha'] != senha:
            raise forms.ValidationError('Senha incorreta')


class ClienteForm(forms.ModelForm):
    class Meta:
        model = BancoUsuarios
        fields = '__all__'


