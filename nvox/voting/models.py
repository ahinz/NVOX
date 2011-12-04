from django.db import models
from django.db.models import Sum

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    descr = models.TextField()
    cost = models.IntegerField()
    complexity = models.IntegerField()
    link = models.TextField()
    location = models.TextField()
    image = models.TextField()

    def votes(self):
        return Vote.objects.filter(project=self.pk).aggregate(Sum('contribution'))["contribution__sum"]

class Vote(models.Model):
    date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=200)
    contribution = models.IntegerField()

    project = models.ForeignKey(Project)
