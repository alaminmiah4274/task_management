from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# many to one relationship
class Task(models.Model):
	# project = models.ForeignKey("Project", on_delete = models.CASCADE, null = True, blank = True)
	# PENDING = "PENDING"
	# IN_PROGRESS = "IN_PROGRESS"
	# COMPLETED = "CCOMPLETED"
	STATUS_CHOICES = [
		("PENDING", "Pending"),
		("IN_PROGRESS", "In Progress"),
		("COMPLETED", "Completed")
	]

	project = models.ForeignKey("Project", on_delete = models.CASCADE, default = 1, related_name = "task")
	# assigned_to = models.ManyToManyField("Employee", related_name = "task")
	assigned_to = models.ManyToManyField(User, related_name = "tasks")
	title = models.CharField(max_length = 250)
	description = models.TextField()
	due_date = models.DateField()
	status = models.CharField(max_length = 15, choices = STATUS_CHOICES, default = "PENDING")
	is_completed = models.BooleanField(default = False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.title

	# TaskDetail --> reverse relation:
	# details


# one to one relationship 
class TaskDetail(models.Model):
	HIGH = "H"
	MEDIUM = "M"
	LOW = "L"
	PRIORITY_OPTIONS = [
		# left: DB -- right: UI
		(HIGH, "HIGH"),
		(MEDIUM, "MEDIUM"),
		(LOW, "LOW")
	]
	# std_id = models.CharField(max_length = 200, primary_key = True) # to make primary key
	# assigned_to = models.CharField(max_length=250)

	asset = models.ImageField(upload_to = "task_asset", blank = True, null = True, default = "task_asset/default_img.jpg")
	task = models.OneToOneField(Task, on_delete = models.DO_NOTHING, related_name = "details")
	priority = models.CharField(max_length = 1, choices = PRIORITY_OPTIONS, default = LOW)
	notes = models.TextField(blank = True, null = True)

	def __str__(self):
		return f"Details from task {self.task.title}"



class Project(models.Model):
	name = models.CharField(max_length = 100)
	description = models.TextField(blank = True, null = True)
	start_date = models.DateField()

	def __str__(self):
		return self.name

	# task_set --> reverse relation:
	# related name: task

"""
to get all projects: p = Project.objects.all()
to get first project: p.first()
to get the id of first project: p.first().id
"""


# class Employee(models.Model):
# 	name = models.CharField(max_length = 100)
# 	email = models.EmailField(unique = True)

# 	# task_set --> reverse relation: 
# 	# related name: task

# 	def __str__(self):
# 		return self.name


"""
TO ADD IMAGE OR MEDIA FILE in Django:

1. install pillow package
2. write these in settings.py file:
--> MEDIA_URL = "/media/" 
--> MEDIA_ROOT = BASE_DIR / "media"

3. write these in urls.py:
--> from django.conf.static import static
--> from django.conf import settings
--> urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

4. add ImageField in the model
5. write this in the html form:
--> enctype="multipart/form-data"

6. include model field in the form of forms.py
7. write this in the views.py:
--> request.FILES
"""