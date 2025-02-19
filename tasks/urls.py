from django.urls import path
from tasks.views import manager_dashboard, employee_dashboard, test_static, create_task, show_task, update_task, delete_task, task_details, dashboard

urlpatterns = [
	path("manager-dashboard/", manager_dashboard, name = "manager-dashboard"),
	path("employee-dashboard/", employee_dashboard, name = "employee-dashboard"),
	path("test/", test_static),
	path("create-task/", create_task, name = "create-task"),
	path("task/<int:task_id>/details", task_details, name = "task-details"),
	path("show-task/", show_task),
	path("update-task/<int:id>/", update_task, name = "update-task"),
	path("delete-task/<int:id>/", delete_task, name = "delete-task"),
	path("dashboard/", dashboard, name = "dashboard")
]