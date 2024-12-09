from django.db import models
import uuid

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Contact(models.Model):
    contactId = models.UUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    add_name = models.CharField(max_length=100)
    add_email = models.EmailField()
    add_phone = models.CharField(max_length=20)
    initials = models.CharField(max_length=5)
    color = models.CharField(max_length=7)

class Task(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('urgent', 'Urgent')],
    )
    status = models.CharField(
        max_length=20,
        choices=[('toDo', 'To Do'), ('inProgress', 'In Progress'), ('done', 'Done'), ('awaitFeedback', 'Await Feedback')],
    )
    subTasks = models.JSONField(default=list)
    contacts = models.JSONField(default=list)