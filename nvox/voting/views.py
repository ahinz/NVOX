from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.middleware.csrf import get_token
from django.template import RequestContext

from voting.models import Project, Vote, Community, CommunityProject

def home(request):
    return home_filter(request, None)

def home_filter(request, community_title):
    
    if community_title is not None:
        community = Community.objects.get(title=community_title)
        projects = [cp.project for cp in CommunityProject.objects.filter(community=community).all()]
        info = "/community/%s/info" % community_title
        vote = "/community/%s" % community_title
    else:
        projects = Project.objects.all()
        info = "/info"
        vote = "/"

    token = get_token(request)

    max_votes = max([p.votes() for p in projects])
    max_cplx = max([p.complexity for p in projects])
    min_cplx = min([p.complexity for p in projects])

    data = { 'projects': projects, 
             'max_votes': max_votes, 
             'community': community_title,
             'max_cplx': max_cplx,
             'min_cplx': min_cplx,
             'info': info,
             'vote': vote }

    resp = render_to_response('voting/index.html', data, context_instance=RequestContext(request))
    resp.set_cookie('csrftoken', token)

    return resp

def home_info_index(request):
    return home_info(request, None)

def home_info(request, community_title):
    
    if community_title is not None:
        community = Community.objects.get(title=community_title)
        projects = [cp.project for cp in CommunityProject.objects.filter(community=community).all()]
        info = "/community/%s/info" % community_title
        vote = "/community/%s" % community_title
    else:
        projects = Project.objects.all()
        info = "/info"
        vote = "/"

    projects = sorted(projects, key=lambda p: p.votes(), reverse=True)

    token = get_token(request)

    max_votes = max([p.votes() for p in projects])
    max_cplx = max([p.complexity for p in projects])
    min_cplx = min([p.complexity for p in projects])

    data = { 'projects': projects, 
             'max_votes': max_votes, 
             'community': community_title,
             'max_cplx': max_cplx,
             'min_cplx': min_cplx,
             'info': info,
             'vote': vote }

    resp = render_to_response('voting/info.html', data, context_instance=RequestContext(request))
    resp.set_cookie('csrftoken', token)

    return resp


def vote_up(request):
    return vote(request,1)

def vote_down(request):
    return vote(request, -1)

def vote(request, amt):
    if request.user is not None and request.user.is_authenticated():
        user = request.user
        req = request.REQUEST

        p = Project.objects.get(pk=req["project"])
        
        votes = Vote.objects.filter(user=user,project=p).all()
        if votes is None or len(votes) == 0:
            vote = Vote(location="!", contribution=amt, project=p, user=user)
        else:
            vote = votes[0]
            vote.contribution = amt

        
        vote.save()
        
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

def logout(request):
    if request.user is not None:
        auth.logout(request)

    return HttpResponse("{ \"success\": \"true\" }", mimetype="application/json")

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
                return HttpResponse("{ \"authorized\": true }")
        else:
            return HttpResponse("{ \"authorized\": false }")
