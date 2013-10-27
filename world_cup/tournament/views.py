from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from tournament.models import *


def index(request):
    return render_to_response('tournament/index.html', context_instance=RequestContext(request))


def brackets(request):
    group_labels = Countries.objects.values('group').distinct()
    groups = []
    for label in group_labels:
        label = label['group']
        groups.append(Countries.objects.filter(group=label))
    matches = MatchWinners.objects.filter(user=request.user)
    return render_to_response('tournament/brackets.html', {'groups': groups, 'matches': matches},
                              context_instance=RequestContext(request))


def save(request):
    if request.method == 'POST':
        if request.POST['type'] == 'add-group':
            country = Countries.objects.get(id=request.POST['country'])
            position = int(request.POST['position'])
            winner = GroupWinners(user=request.user, country=country, position=position)
            winner.save()
            return HttpResponse('saved')
        elif request.POST['type'] == 'remove-group':
            country = Countries.objects.get(id=request.POST['country'])
            winner = GroupWinners.objects.get(country=country)
            winner.delete()
            return HttpResponse('removed')
