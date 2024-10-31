from django.db import models


class Note(models.Model):
    class Category(models.IntegerChoices):
        TECHNICAL_TASK = 1, 'Technical Task'
        USER_STORY = 2, 'User Story'

    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        URGENT = 3, 'Urgent'

    category = models.PositiveSmallIntegerField(choices=Category.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    prio = models.PositiveSmallIntegerField(choices=Priority.choices)
    # contacts = models.ManyToManyField(Contact, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
        
class Subtask(models.Model):
    note = models.ForeignKey(Note, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']