from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class CadastroUsuarioForm(UserCreationForm):
    nome = forms.CharField(
        label="Nome",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu nome",
            }
        ),
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu e-mail",
            }
        ),
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme sua senha",
            }
        ),
    )

    class Meta:
        model = Usuario
        fields = ("nome", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada com este e-mail.")

        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data["email"].lower()
        usuario.email = self.cleaned_data["email"].lower()
        usuario.nome = self.cleaned_data["nome"]

        if commit:
            usuario.save()

        return usuario