from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.FloatField(default=1.0)
    importance = models.IntegerField(default=5)
    
    def __str__(self):
        return self.title