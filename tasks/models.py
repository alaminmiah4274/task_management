from django.db import models

# Create your models here.

# manay to one relationship
class Task(models.Model):
	# project = models.ForeignKey("Project", on_delete = models.CASCADE, null = True, blank = True)

	project = models.ForeignKey("Project", on_delete = models.CASCADE, default = 1, related_name = "task")
	assigned_to = models.ManyToManyField("Employee", related_name = "task")
	title = models.CharField(max_length = 250)
	description = models.TextField()
	due_date = models.DateField()
	is_completed = models.BooleanField(default = False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	# taskdetail --> reverse relation:
	# details


# one to one relationship 
class TaskDetail(models.Model):
	HIGH = "H"
	MEDIUM = "M"
	LOW = "L"
	PRIORITY_OPTIONS = (
		(HIGH, "HIGH"),
		(MEDIUM, "MEDIUM"),
		(LOW, "LOW")
	)
	task = models.OneToOneField(Task, on_delete = models.CASCADE, related_name = "details")
	assigned_to = models.CharField(max_length = 250)
	priority = models.CharField(max_length = 1, choices = PRIORITY_OPTIONS, default = LOW)



class Project(models.Model):
	name = models.CharField(max_length = 100)
	start_date = models.DateField()

	# task_set --> reverse relation:
	# related name: task

"""
to get all proejcts: p = Project.objects.all()
to get first project: p.first()
to get the id of first project: p.first().id
"""


class Employee(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField(unique = True)

	# tast_set --> reverse relation: 
	# related name: task

	def __str__(self):
		return self.name