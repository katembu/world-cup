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
    return render_to_response('tournament/brackets.html', {'groups': groups}, context_instance=RequestContext(request))
