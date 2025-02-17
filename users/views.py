from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from users.forms import SignUpForm, CustomSignUpForm, SignInForm, AssignRoleForm, CreateGroupModelForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch


# Create your views here.


# test for users:
def is_admin(user):
	return user.groups.filter(name = "Admin").exists()


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
			# 	User.objects.create(username = user_name, password = password)

			user = form.save(commit = False)
			user.set_password(form.cleaned_data.get("password1"))
			user.is_active = False
			user.save()

			messages.success(request, "A confirmation mail has sent. Please check your email")
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
		# 	login(request, user)
		# 	return redirect("home")

		form = SignInForm(data = request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect("home")


	context = {
		"form": form
	}

	return render(request, "registration/sign_in.html", context)


@login_required
def sign_out(request):
	if request.method == "POST":
		logout(request)
		return redirect("sign-in")

	return render(request, "home.html")



def activate_user(request, user_id, token):
	try:
		user = User.objects.get(id = user_id)

		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			return redirect("sign-in")
		else:
			return HttpResponse("Invalid id or token")
	except User.DoesNotExist:
		return HttpResponse("User Not Found!")



@user_passes_test(is_admin, login_url = "no-permission")
def admin_dashboard(request):

	''' 1st WAY ''' 
	# users = User.objects.all()


	''' 2nd WAY '''
	# users = User.objects.prefetch_related("groups").all()


	# for user in users:
	# 	if user.groups.exists():
	# 		user.group_name = user.groups.first().name
	# 	else:
	# 		user.group_name = "No Group Assigned"


	""" 3ed WAY """
	users = User.objects.prefetch_related(
		Prefetch("groups", queryset = Group.objects.all(), to_attr = "all_groups")
	).all()

	for user in users:
		if user.all_groups:
			user.group_name = user.all_groups[0].name
		else:
			user.group_name = "No Group Assigned"


	context = {
		"users": users
	}

	return render(request, "admin/dashboard.html", context)



@user_passes_test(is_admin, login_url = "no-permission")
def assign_role(request, user_id):
	user = User.objects.get(id = user_id)
	form = AssignRoleForm()
	
	if request.method == "POST":
		form = AssignRoleForm(request.POST)
		if form.is_valid():
			role = form.cleaned_data.get("role")
			user.groups.clear()
			user.groups.add(role)

			messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
			return redirect("admin-dashboard")


	context = {
		"form": form
	}

	return render(request, "admin/assign_role.html", context)



@user_passes_test(is_admin, login_url = "no-permission")
def create_group(request):
	form = CreateGroupModelForm()

	if request.method == "POST":
		form = CreateGroupModelForm(request.POST)

		if form.is_valid():
			group = form.save()

			messages.success(request, f"Group {group.name} has been created successfully")
			return redirect("create-group")

	context = {
		"form": form
	}

	return render(request, "admin/create_group.html", context)



@user_passes_test(is_admin, login_url = "no-permission")
def group_list(request):
	groups = Group.objects.prefetch_related("permissions").all()

	context = {
		"groups": groups
	}

	return render(request, "admin/group_list.html", context)



# john_doe: Aus@2024 
# the_rock: Aus@2024
# the_hammer: Ban@2024
# chris_brook: Ban@2024
# chris_pattern: Doe@2024 | employee
# bad_boy: Doe@2024 | user
# shafim_rahman: Man@2024 | manager