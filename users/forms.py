from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user is not None:
                if user.check_password(password):
                    return self.cleaned_data
                else:
                    self.add_error("password", "Password is wrong")
        except models.User.DoesNotExist:
            self.add_error("email", "Email is not exist")


class SignupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="confirm password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password == password1:
            return password1
        else:
            raise forms.ValidationError("password does not match")

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
