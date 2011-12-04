from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.template import RequestContext

from voting.models import Project, Vote

def home(request):
    projects = Project.objects.all()

    token = get_token(request)

    resp = render_to_response('voting/index.html', { 'projects': projects }, context_instance=RequestContext(request))
    resp.set_cookie('csrftoken', token)

    return resp

def vote_up(request):
    return vote(request,1)

def vote_down(request):
    return vote(request, -1)

def vote(request, amt):
    if request.user is not None and request.user.is_authenticated():
        req = request.REQUEST
        
        p = Project.objects.get(pk=req["project"])
        v = Vote(location="!", contribution=amt, project=p)
        
        v.save()
        
        if req["format"] == "json":
            return HttpResponse("{ \"success\": true, \"votes\": %s }" % p.votes(), mimetype="application/json")
        else:
            return redirect('/')
    else:
        return HttpResponse("{ \"success\": false }",mimetype="application/json")


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

def login_user(request):
    username = password = ''

    if request.POST or True:
        username = request.POST.get('username')
        password = request.POST.get('password')

        print "got username/pw: %s / %s".format(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("authorized")
        else:
            return HttpResponse("unauthorized")
