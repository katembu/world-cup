from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from user_management.forms import *
from tournament.helpers import create_matches


def login_user(request):
    logout(request)
    username = password = ''
    user = None
    next = request.GET['next'] if 'next' in request.GET else None
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']
        user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        return HttpResponseRedirect('%s' % next if next != 'None' else '/')
    return render_to_response('login.html', {'next': next, }, context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect('user_management.views.index')


def create_user(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    return render_to_response('create_user.html', {'form': form},
                              context_instance=RequestContext(request))


def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))
