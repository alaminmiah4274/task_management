from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, test_static

urlpatterns = [
	path("manager-dashboard/", manager_dashboard),
	path("user-dashboard/", user_dashboard),
	path("test/", test_static),
]