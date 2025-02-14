from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.

# many to one relationship
class Task(models.Model):
	# project = models.ForeignKey("Project", on_delete = models.CASCADE, null = True, blank = True)
	# PENDING = "PENDING"
	# IN_PROGRESS = "IN_PROGRESS"
	# COMPLETED = "CCOMPLETED"
	STATUS_CHOICES = {
		("PENDING", "Pending"),
		("IN_PROGRESS", "In Progress"),
		("COMPLETED", "Completed")
	}

	project = models.ForeignKey("Project", on_delete = models.CASCADE, default = 1, related_name = "task")
	assigned_to = models.ManyToManyField("Employee", related_name = "task")
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
	PRIORITY_OPTIONS = (
		(HIGH, "HIGH"),
		(MEDIUM, "MEDIUM"),
		(LOW, "LOW")
	)
	# std_id = models.CharField(max_length = 200, primary_key = True) # to make primary key
	# assigned_to = models.CharField(max_length=250)


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


class Employee(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField(unique = True)

	# task_set --> reverse relation: 
	# related name: task

	def __str__(self):
		return self.name



# signal
# @receiver(post_save, sender = Task)
# def notify_task_creation(sender, instance, created, **kwargs):
# 	print("sender:", sender)
# 	print("instance:", instance)
# 	print(kwargs)
# 	print("created:", created)

# 	if created:
# 		instance.is_completed = True
# 		instance.save()


# @receiver(pre_save, sender = Task)
# def notify_task_creation(sender, instance, **kwargs):
# 	print("sender:", sender)
# 	print("instance:", instance)
# 	print(kwargs)

# 	instance.is_completed = True

@receiver(m2m_changed, sender = Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
	if action == "post_add":
		assigned_email = [emp.email for emp in instance.assigned_to.all()]

		send_mail(
			"New Task Assigned",
			f"You have been assigned to the task: {instance.title}",
			"alaminmiah4274@gmail.com",
			assigned_email,
			fail_silently = False
		)


@receiver(post_delete, sender = Task)
def delete_associated_details(sender, instance, **kwargs):
	if instance.details:
		print(instance)

		instance.details.delete()
		print("task deleted...")