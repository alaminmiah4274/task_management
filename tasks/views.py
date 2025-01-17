from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def manager_dashboard(request):
	return render(request, "dashboard/manager_dashboard.html")


def user_dashboard(request):
	return render(request, "dashboard/user_dashboard.html")


def test_static(request):

	names = ["miah", "howlader", "billah", "shafim", "sheikh"]
	
	count = 0
	for name in names:
		count += 1

	context = {
		"names": names,
		"ages": [23, 25, 27, 23, 25],
		"count": count,
	}

	return render(request, "test.html", context)