from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from users.forms import (
    CustomSignUpForm,
    SignInForm,
    AssignRoleForm,
    CreateGroupModelForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomPasswordResetConfirmForm,
    EditProfileForm,
)
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View


User = get_user_model()


# test for users:
def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def sign_up(request):
    form = CustomSignUpForm()

    if request.method == "POST":
        form = CustomSignUpForm(request.POST)

        if form.is_valid():
            # form.save()
            # user_name = form.cleaned_data.get("username")
            # password = form.cleaned_data.get("password1")
            # confirm_password = form.cleaned_data.get("password2")

            # if password == confirm_password:
            #   User.objects.create(username = user_name, password = password)

            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.is_active = False
            user.save()

            messages.success(
                request, "A confirmation mail has sent. Please check your email"
            )
            return redirect("sign-in")

    # pass: Ban@2024
    return render(request, "registration/sign_up.html", {"form": form})


def sign_in(request):
    form = SignInForm()

    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")

        # user = authenticate(request, username = username, password = password)

        # if user is not None:
        #   login(request, user)
        #   return redirect("home")

        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    context = {"form": form}

    return render(request, "registration/sign_in.html", context)


class CustomSignInView(LoginView):
    form_class = SignInForm

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        return next_url if next_url else super().get_success_url()


@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")

    return render(request, "home.html")


# SIGN OUT CLASS VIEW:
class CustomSignOutView(LoginRequiredMixin, LogoutView):
    login_url = "no-permission"
    next_page = reverse_lazy("sign-in")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User Not Found!")


@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    """1st WAY"""
    # users = User.objects.all()

    """ 2nd WAY """
    # users = User.objects.prefetch_related("groups").all()

    # for user in users:
    #   if user.groups.exists():
    #       user.group_name = user.groups.first().name
    #   else:
    #       user.group_name = "No Group Assigned"

    """ 3ed WAY """
    users = User.objects.prefetch_related(
        Prefetch("groups", queryset=Group.objects.all(), to_attr="all_groups")
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assigned"

    context = {"users": users}

    return render(request, "admin/dashboard.html", context)


@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)

            messages.success(
                request,
                f"User {user.username} has been assigned to the {role.name} role",
            )
            return redirect("admin-dashboard")

    context = {"form": form}

    return render(request, "admin/assign_role.html", context)


# ASSIGN ROLE CLASS VIEW:
class AssignRoleView(UserPassesTestMixin, View):
    login_url = "no-permission"
    template_name = "admin/assign_role.html"

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request, *args, **kwargs):
        form = AssignRoleForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        form = AssignRoleForm(request.POST)
        user = User.objects.get(id=user_id)

        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)

            messages.success(
                request,
                f"User {user.username} has been assigned to the {role.name} role",
            )
            return redirect("admin-dashboard")

        context = {"form": form}
        return render(request, self.template_name, context)


@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    form = CreateGroupModelForm()

    if request.method == "POST":
        form = CreateGroupModelForm(request.POST)

        if form.is_valid():
            group = form.save()

            messages.success(
                request, f"Group {group.name} has been created successfully"
            )
            return redirect("create-group")

    context = {"form": form}

    return render(request, "admin/create_group.html", context)


# CREATE GROUP CLASS VIEW:
class CreateGroupView(UserPassesTestMixin, CreateView):
    login_url = "no-permission"
    form_class = CreateGroupModelForm
    template_name = "admin/create_group.html"
    success_url = reverse_lazy("create-group")

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request, f"Group {self.object.name} has been created successfully"
        )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context


@user_passes_test(is_admin, login_url="no-permission")
def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()

    context = {"groups": groups}

    return render(request, "admin/group_list.html", context)


# GROUP LIST CLASS VIEW:
class GroupListView(UserPassesTestMixin, ListView):
    model = Group
    template_name = "admin/group_list.html"
    login_url = "no-permission"
    context_object_name = "groups"

    def test_func(self):
        return is_admin(self.request.user)

    def get_queryset(self):
        return Group.objects.prefetch_related("permissions").all()


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["username"] = user.username
        context["email"] = user.email
        context["name"] = user.get_full_name()
        context["member_since"] = user.date_joined
        context["last_login"] = user.last_login
        context["bio"] = user.bio
        context["profile_image"] = user.profile_image

        return context


class ChangePassword(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/reset_password.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("sign-in")
    html_email_template_name = "registration/reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, "A reset email sent. Please check your email")
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/reset_password.html"
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        messages.success(self.request, "Password has been reset successfully")
        return super().form_valid(form)


"""
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "accounts/update_profile.html"
    context_object_form = "form"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["userprofile"] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context["form"] = self.form_class(
            instance=self.object, userprofile=user_profile
        )

        return context

    def form_save(self, form):
        form.save(commit=True)
        return super().form_valid(form)
"""


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "accounts/update_profile.html"
    context_object_form = "form"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def form_save(self, form):
        form.save()
        return super().form_save(form)


# john_doe: Aus@2024 | active
# the_hammer: Ban@2024 | active
# chris_brook: Ban@2024 | active
# chris_pattern: Doe@2024-->Change@2024 | employee
# bad_boy: Doe@2024-->Bad@2024 | user
# shafim_rahman: Man@2024 | manager
# admin: 1234 | admin
# donald_obama: Bama@2024 | user
# elon_trump: Lon@2024 | user
# dr_yunus: Nus@2024 | user
