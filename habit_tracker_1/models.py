from django.db import models

class Habit(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completion_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
