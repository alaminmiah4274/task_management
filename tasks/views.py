from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task, Project
from datetime import date, timedelta
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import (
    user_passes_test,
    login_required,
    permission_required,
)
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView


# class based view re-use example:
class Greetings(View):
    greetings = "Hello, Everyone"

    def get(self, request):
        return HttpResponse(self.greetings)


class HiGreetings(Greetings):
    greetings = "Hi, Everyone...."


class HowGreetings(Greetings):
    greetings = "How are you everyone"


# test decorator for manager:
def is_manager(user):
    return user.groups.filter(name="Manager").exists()


def is_employee(user):
    return user.groups.filter(name="Employee").exists()


@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def manager_dashboard(request):
    type = request.GET.get("type", "all")

    # tasks = Task.objects.select_related("details").prefetch_related("assigned_to").all()

    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status = "COMPLETED").count()
    # in_progress_task = Task.objects.filter(status = "IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status = "PENDING").count()

    counts = Task.objects.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="COMPLETED")),
        in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
        pending=Count("id", filter=Q(status="PENDING")),
    )

    # retrieving card data (dynamic query)
    base_query = Task.objects.select_related("details").prefetch_related("assigned_to")

    if type == "completed":
        tasks = base_query.filter(status="COMPLETED")
    elif type == "in-progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == "pending":
        tasks = base_query.filter(status="PENDING")
    elif type == "all":
        tasks = base_query.all()

    # context = {
    #   "tasks": tasks,
    #   "total_task": total_task,
    #   "completed_task": completed_task,
    #   "in_progress_task": in_progress_task,
    #   "pending_task": pending_task
    # }

    context = {"tasks": tasks, "counts": counts}

    return render(request, "dashboard/manager_dashboard.html", context)


@login_required
@permission_required("tasks.view_task", login_url="no-permission")
def employee_dashboard(request):
    return render(request, "dashboard/employee_dashboard.html")


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


# task is being created with task form
@login_required
@permission_required("tasks.add_task", login_url="no-permission")
def create_task(request):
    # for GET:
    # employees = Employee.objects.all()
    # form = TaskForm(employees = employees)
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    # for POST:
    if request.method == "POST":
        """for Django Model Form"""
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task created successfully")
            return redirect("create-task")

        """ for Django Form """
        # form = TaskForm(request.POST, employees = employees)
        # if form.is_valid():
        #   data = form.cleaned_data
        #   title = data.get("title")
        #   description = data.get("description")
        #   due_date = data.get("due_date")
        #   assigned_to = data.get("assigned_to")

        #   task = Task.objects.create(title = title, description = description, due_date = due_date)

        #   for emp_id in assigned_to:
        #       employee = Employee.objects.get(id = emp_id)
        #       task.assigned_to.add(employee)

        #   return HttpResponse("Task Added Successfully")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


create_task_decorators = [
    login_required,
    permission_required("tasks.add_task", login_url="no-permission"),
]


class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """Creating for tasks"""

    permission_required = "tasks.add_task"
    login_url = "sign-in"
    template_name = "task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_form"] = kwargs.get("task_form", TaskModelForm())
        context["task_detail_form"] = kwargs.get(
            "task_detail_form", TaskDetailModelForm()
        )
        return context

    def get(self, request, *args, **kwargs):
        # task_form = TaskModelForm()
        # task_detail_form = TaskDetailModelForm()

        # context = {"task_form": task_form, "task_detail_form": task_detail_form}
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task.save()

            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(
                task_form=task_form, task_detail_form=task_detail_form
            )
            return render(request, self.template_name, context)


def show_task(request):
    # tasks = Task.objects.all()

    # load specific task:
    # task_3 = Task.objects.get(id = 1)
    # task_3 = Task.objects.get(pk = 3)
    # task_3 = Task.objects.get(title = "Key data character house.")
    # task_3 = Task.objects.get(status = "COMPLETED")

    # getting first element:
    # first_task = Task.objects.first();

    """only filtering"""
    # tasks = Task.objects.filter(status = "PENDING")
    # tasks = Task.objects.filter(status = "COMPLETED")

    """ SHOWING THE TASKS WHOSE DUE DATE IS TODAY """
    # tasks = Task.objects.filter(due_date = date.today())

    """ SHOWING THE TASK WHOSE PRIORITY IS NOT LOW """
    # tasks = TaskDetail.objects.exclude(priority = "L")

    """ SHOW THE TASK THAT CONTAINS THE WROD 'PAPER' """
    # tasks = Task.objects.filter(id__gt = 18)
    # tasks = Task.objects.filter(title__icontains = "c", status = "PENDING")
    # tasks = Task.objects.filter(Q(status = "PENDING") | Q(status = "IN_PROGRESS"))

    # tasks = Task.objects.filter(title = "alsdkfalsf").exists()

    """ QUERY OPTIMIZE WAY ---> RELATED DATA QUERY """
    # select_related(ForeignKey, OneToOneField)
    # tasks = Task.objects.all()
    """ relation between Task and TaskDetail for OneToOneField """
    # tasks = Task.objects.select_related("details").all()

    """ relation between TaskDetail and Task for OneToOneField """
    # tasks = TaskDetail.objects.select_related("task").all()

    """ relation between Project and Task for ForeignKey """
    # tasks = Task.objects.select_related("project").all()

    # prefetch_related(ManyToManyField, riverse ForeignKey)
    """ riverse ForeignKey """
    # tasks = Project.objects.prefetch_related("task").all()

    """ ManyToManyField """
    # tasks = Task.objects.prefetch_related("assigned_to").all()
    """ reverse way """
    # tasks = Employee.objects.prefetch_related("task").all()

    """ AGGREGATION """
    # Count(), Sum(), Avg(), Min(), Max()
    # task_count = Task.objects.aggregate(num_task = Count("id"))
    """ ascedging order """
    # projects = Project.objects.annotate(task_nums = Count("task")).order_by("task_nums")

    tasks = Task.objects.filter(due_date__lt=date.today() - timedelta(weeks=1))

    """ descending order """
    # projects = Project.objects.annotate(task_nums = Count("task")).order_by("-task_nums")

    return render(request, "show_task.html", {"tasks": tasks})
    # return render(request, "show_task.html", {"tasks": tasks, "task_3": task_3, "first_task": first_task})


show_project_decorators = [
    login_required,
    permission_required("tasks.view_project", login_url="no-permission"),
]


@method_decorator(show_project_decorators, name="dispatch")
class ShowProject(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "show_task.html"

    def get_queryset(self):
        queryset = Project.objects.annotate(task_nums=Count("task")).order_by(
            "task_nums"
        )
        return queryset


@login_required
@permission_required("tasks.change_task", login_url="no-permission")
def update_task(request, id):
    task = Task.objects.get(id=id)

    task_form = TaskModelForm(instance=task)

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=task.details
        )

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect("update-task", id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = "task_form.html"
    conext_object_name = "task"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_form"] = self.get_form()

        if hasattr(self.object, "details") and self.object.details:
            context["task_detail_form"] = TaskDetailModelForm(
                instance=self.object.details
            )
        else:
            context["task_detail_form"] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)
        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, "details", None)
        )

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect("update-task", self.object.id)
        else:
            return redirect("update-task", self.object.id)


@login_required
@permission_required("tasks.delete_task", login_url="no-permission")
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()

        messages.success(request, "Task Deleted Successfully")
        return redirect("manager-dashboard")
    else:
        messages.error(request, "Something Went Wrong")
        return redirect("manager-dashboard")


@login_required
@permission_required("task.change_task", login_url="no-permission")
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == "POST":
        selected_status = request.POST.get("task_status")
        task.status = selected_status
        task.save()

        return redirect("task-details", task.id)

    context = {"task": task, "status_choices": status_choices}

    return render(request, "task_details.html", context)


# task details class view
class TaskDetail(DetailView):
    model = Task
    template_name = "task_details.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get("task_status")
        task.status = selected_status
        task.save()
        return redirect("task-details", task.id)


@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect("manager-dashboard")
    elif is_employee(request.user):
        return redirect("employee-dashboard")
    elif is_admin(request.user):
        return redirect("admin-dashboard")

    return redirect("no-permission")
