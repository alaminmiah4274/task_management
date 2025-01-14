from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	# work with database
	# transform data
	# data pass
	# http response / json response return
	return HttpResponse("Welcome to the task management system")


def contact(request):
	return HttpResponse("<h1 style='color: red'>this is contact page response ...<h1>")


def show_task(request):
	return HttpResponse("this is task page")