from django.db import models
from django.db.models import Sum, Count
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    descr = models.TextField()
    cost = models.IntegerField()
    complexity = models.IntegerField()
    link = models.TextField()
    location = models.TextField()
    image = models.TextField()

    def __unicode__(self):
        return self.title

    def votes_up(self):
        return Vote.objects.filter(project=self.pk,contribution__gt=0).aggregate(Count('contribution'))["contribution__count"]

    def votes_down(self):
        return Vote.objects.filter(project=self.pk,contribution__lt=0).aggregate(Count('contribution'))["contribution__count"]

    def votes(self):
        return Vote.objects.filter(project=self.pk).aggregate(Sum('contribution'))["contribution__sum"]

class Community(models.Model):
    title = models.TextField()

    def __unicode__(self):
        return self.title

class CommunityProject(models.Model):
    community = models.ForeignKey(Community)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "%s <--> %s" % (self.community, self.project)

class Vote(models.Model):
    date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=200)
    contribution = models.IntegerField()

    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
