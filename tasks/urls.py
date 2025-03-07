from django.urls import path
from tasks.views import (
    manager_dashboard,
    ManagerDashboardView,
    employee_dashboard,
    EmployeeDashboardView,
    test_static,
    create_task,
    show_task,
    update_task,
    delete_task,
    task_details,
    dashboard,
    Greetings,
    HiGreetings,
    HowGreetings,
    CreateTask,
    ShowProject,
    TaskDetail,
    UpdateTask,
    TaskDeleteView,
)

urlpatterns = [
    path(
        "manager-dashboard/", ManagerDashboardView.as_view(), name="manager-dashboard"
    ),
    path(
        "employee-dashboard/",
        EmployeeDashboardView.as_view(),
        name="employee-dashboard",
    ),
    path("test/", test_static),
    path("create-task/", CreateTask.as_view(), name="create-task"),
    # path("task/<int:task_id>/details", task_details, name="task-details"),
    path("task/<int:task_id>/details", TaskDetail.as_view(), name="task-details"),
    # path("show-task/", show_task, name="show-task"),
    path("show-task/", ShowProject.as_view(), name="show-task"),
    # path("update-task/<int:id>/", update_task, name="update-task"),
    path("update-task/<int:id>/", UpdateTask.as_view(), name="update-task"),
    path("delete-task/<int:id>/", TaskDeleteView.as_view(), name="delete-task"),
    path("dashboard/", dashboard, name="dashboard"),
    path(
        "greetings/",
        HowGreetings.as_view(greetings="How good day today!"),
        name="greetings",
    ),
]
