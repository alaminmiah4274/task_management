from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project, Employee
from datetime import date
from django.db.models import Q, Count, Min, Max, Avg, Sum

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


def create_task(request):

	# for GET:
	# employees = Employee.objects.all()
	# form = TaskForm(employees = employees)
	form = TaskModelForm()

	# for POST:
	if request.method == "POST":
		""" for Django Model Form """
		form = TaskModelForm(request.POST)
		if form.is_valid():
			form.save()

			return render(request, "task_form.html", {"form": form, "message": "Task added successfully"})


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


	context = {"form": form}
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
	projects = Project.objects.annotate(task_nums = Count("task")).order_by("task_nums")

	''' descending order '''
	# projects = Project.objects.annotate(task_nums = Count("task")).order_by("-task_nums")

	return render(request, "show_task.html", {"projects": projects})
	# return render(request, "show_task.html", {"tasks": tasks, "task_3": task_3, "first_task": first_task})