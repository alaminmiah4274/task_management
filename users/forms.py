from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import Group, Permission
from django import forms
import re
from tasks.forms import StyledFormMixin
from django.core.exceptions import ValidationError
from users.models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["username"].help_text = None

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None


class CustomSignUpForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "confirm_password",
            "email",
        ]

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        errors = []

        if len(password1) < 8:
            # raise forms.ValidationError("Password must be at least 8 characters long")
            errors.append("Password must be at least 8 characters long")

        if re.fullmatch(r"[A-Za-z0-9!@#$%^&*+=]", password1):
            # raise forms.ValidationError("Password must be at least 8 characters, Uppercase, Lowercase, number & spacial characters")
            errors.append(
                "Password must be Uppercase, Lowercase, Number & special characters"
            )

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exist = User.objects.filter(email=email).exists()

        if email_exist:
            raise ValidationError("The email is already in use")

        return email


class SignInForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(), empty_label="Select A Role"
    )


class CreateGroupModelForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Assign Group",
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass


"""
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    bio = forms.CharField(required=False, label="bio")
    profile_image = forms.ImageField(required=False, label="profile_image")

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop("userprofile", None)
        super().__init__(*args, **kwargs)

        # handle error:

        if self.userprofile:
            self.fields["bio"].initial = self.userprofile.bio
            self.fields["profile_image"].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)

        # if user is exits than save it:
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get("bio")
            self.userprofile.profile_image = self.cleaned_data.get("profile_image")

            if commit:
                self.userprofile.save()

        if commit:
            user.save()

        return user
"""


class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "bio", "profile_image"]
