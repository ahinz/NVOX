from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from voting.models import Project, Vote

def home(request):
    projects = Project.objects.all()

    return render_to_response('voting/index.html', { 'projects': projects })

def vote_up(request):
    return vote(request,1)

def vote_down(request):
    return vote(request, -1)

def vote(request, amt):
    req = request.REQUEST

    p = Project.objects.get(pk=req["project"])

    print "Amt: %s" % amt
    v = Vote(location="!", contribution=amt, project=p)

    v.save()

    return redirect('/')

def create(request):
    req = request.REQUEST

    project = Project(title=req["title"], 
                      descr=req["description"], 
                      cost=int(req["cost"]), 
                      complexity=int(req["complexity"]), 
                      link=req["link"], 
                      location=req["loc"],
                      image=req["image"])

    project.save()

    return redirect('/')
