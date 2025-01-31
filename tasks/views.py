from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project, Employee
from datetime import date, timedelta
from django.db.models import Q, Count, Min, Max, Avg, Sum
from django.contrib import messages

# Create your views here.

def manager_dashboard(request):
	type = request.GET.get("type", "all")

	# tasks = Task.objects.select_related("details").prefetch_related("assigned_to").all()

	# total_task = tasks.count()
	# completed_task = Task.objects.filter(status = "COMPLETED").count()
	# in_progress_task = Task.objects.filter(status = "IN_PROGRESS").count()
	# pending_task = Task.objects.filter(status = "PENDING").count()


	counts = Task.objects.aggregate(
		total = Count("id"),
		completed = Count("id", filter = Q(status = "COMPLETED")),
		in_progress = Count("id", filter = Q(status = "IN_PROGRESS")),
		pending = Count("id", filter = Q(status = "PENDING"))
	)

	# retrieving card data (dynamic query)
	base_query = Task.objects.select_related("details").prefetch_related("assigned_to")


	if type == "completed":
		tasks = base_query.filter(status = "COMPLETED")
	elif type == "in-progress":
		tasks = base_query.filter(status = "IN_PROGRESS")
	elif type == "pending":
		tasks = base_query.filter(status = "PENDING")
	elif type == "all":
		tasks = base_query.all()


	# context = {
	# 	"tasks": tasks,
	# 	"total_task": total_task,
	# 	"completed_task": completed_task,
	# 	"in_progress_task": in_progress_task,
	# 	"pending_task": pending_task
	# }

	context = {
		"tasks": tasks,
		"counts": counts
	}

	return render(request, "dashboard/manager_dashboard.html", context)


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


# task is being created with task form
def create_task(request):

	# for GET:
	# employees = Employee.objects.all()
	# form = TaskForm(employees = employees)
	task_form = TaskModelForm()
	task_detail_form = TaskDetailModelForm()


	# for POST:
	if request.method == "POST":
		""" for Django Model Form """
		task_form = TaskModelForm(request.POST)
		task_detail_form = TaskDetailModelForm(request.POST)

		if task_form.is_valid() and task_detail_form.is_valid():
			task = task_form.save()
			task_detail = task_detail_form.save(commit = False)
			task_detail.task = task
			task_detail.save()

			messages.success(request, "Task created successfully")
			return redirect("create-task")


		''' for Django Form '''
		# form = TaskForm(request.POST, employees = employees)
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	title = data.get("title")
		# 	description = data.get("description")
		# 	due_date = data.get("due_date")
		# 	assigned_to = data.get("assigned_to")

		# 	task = Task.objects.create(title = title, description = description, due_date = due_date)

		# 	for emp_id in assigned_to:
		# 		employee = Employee.objects.get(id = emp_id)
		# 		task.assigned_to.add(employee)

		# 	return HttpResponse("Task Added Successfully")


	context = {"task_form": task_form, "task_detail_form": task_detail_form}
	return render(request, "task_form.html", context)



def show_task(request):
	# tasks = Task.objects.all()

	# load specific task:
	# task_3 = Task.objects.get(id = 1)
	# task_3 = Task.objects.get(pk = 3)
	# task_3 = Task.objects.get(title = "Key data character house.")
	# task_3 = Task.objects.get(status = "COMPLETED")

	# getting first element:
	# first_task = Task.objects.first();

	""" only filtering """
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
	''' relation between Task and TaskDetail for OneToOneField '''
	# tasks = Task.objects.select_related("details").all()

	''' relation between TaskDetail and Task for OneToOneField '''
	# tasks = TaskDetail.objects.select_related("task").all()

	''' relation between Project and Task for ForeignKey '''
	# tasks = Task.objects.select_related("project").all()


	# prefetch_related(ManyToManyField, riverse ForeignKey)
	''' riverse ForeignKey '''
	# tasks = Project.objects.prefetch_related("task").all()

	''' ManyToManyField '''
	# tasks = Task.objects.prefetch_related("assigned_to").all()
	''' reverse way '''
	# tasks = Employee.objects.prefetch_related("task").all()



	""" AGGREGATION """
	# Count(), Sum(), Avg(), Min(), Max()
	# task_count = Task.objects.aggregate(num_task = Count("id"))
	''' ascedging order '''
	# projects = Project.objects.annotate(task_nums = Count("task")).order_by("task_nums")
	
	tasks = Task.objects.filter(due_date__lt = date.today() - timedelta(weeks = 1))

	''' descending order '''
	# projects = Project.objects.annotate(task_nums = Count("task")).order_by("-task_nums")

	return render(request, "show_task.html", {"tasks": tasks})
	# return render(request, "show_task.html", {"tasks": tasks, "task_3": task_3, "first_task": first_task})



def update_task(request, id):
	task = Task.objects.get(id = id)

	task_form = TaskModelForm(instance = task)

	if task.details:
		task_detail_form = TaskDetailModelForm(instance = task.details)

	if request.method == "POST":
		task_form = TaskModelForm(request.POST, instance = task)
		task_detail_form = TaskDetailModelForm(request.POST, instance = task.details)

		if task_form.is_valid() and task_detail_form.is_valid():
			task = task_form.save()
			task_detail = task_detail_form.save(commit = False)
			task_detail.task = task
			task_detail.save()

			messages.success(request, "Task Updated Successfully")
			return redirect("update-task", id)

	context = {"task_form": task_form, "task_detail_form": task_detail_form}
	return render(request, "task_form.html", context)


def delete_task(request, id):
	if request.method == "POST":
		task = Task.objects.get(id = id)
		task.delete()

		messages.success(request, "Task Deleted Successfully")
		return redirect("manager-dashboard")
	else:
		messages.error(request, "Something Went Wrong")
		return redirect("manager-dashboard")