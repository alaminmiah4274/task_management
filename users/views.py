from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from users.forms import SignUpForm, CustomSignUpForm, SignInForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator 


# Create your views here.
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


def sign_out(request):
	if request.method == "POST":
		logout(request)
		return redirect("sign-in")



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


# john_doe: Aus@2024 
# the_rock: Aus@2024
# the_hammer: Ban@2024
# chris_brook: Ban@2024