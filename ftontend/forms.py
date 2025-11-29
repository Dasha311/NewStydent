from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(self.request, username=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный email или пароль.")
        return cleaned_data

    def get_user(self):
        return self.user


class RegistrationForm(forms.Form):
    full_name = forms.CharField(label="ФИО", max_length=255)
    email = forms.EmailField(label="Электронная почта")
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Используйте буквы, цифры и символы.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )
    accept_terms = forms.BooleanField(
        label="Согласие с условиями использования", required=True
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Аккаунт с таким email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли не совпадают.")

        if password1:
            try:
                validate_password(password1, User(username=cleaned_data.get("email")))
            except ValidationError as exc:
                self.add_error("password1", exc)

        return cleaned_data

    def save(self):
        full_name = self.cleaned_data["full_name"].strip()
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]

        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=full_name,
        )
        user.set_password(password)
        user.save()
        return user