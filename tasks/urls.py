from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, test_static, create_task, show_task, update_task, delete_task

urlpatterns = [
	path("manager-dashboard/", manager_dashboard, name = "manager-dashboard"),
	path("user-dashboard/", user_dashboard),
	path("test/", test_static),
	path("create-task/", create_task, name = "create-task"),
	path("show-task/", show_task),
	path("update-task/<int:id>/", update_task, name = "update-task"),
	path("delete-task/<int:id>/", delete_task, name = "delete-task"),
]