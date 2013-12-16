from django.http import *
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from user_management.forms import *
from user_management.models import UserMessages
from tournament.helpers import create_matches
import json


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


def donate(request):
    return render_to_response('donate.html', context_instance=RequestContext(request))


def messages(request):
    if 'id' in request.GET:
        message = get_object_or_404(UserMessages, id=request.GET['id'], to=request.user)
        message.read = True
        message.save()
        return render_to_response('user_management/messages.html', {'message': message, },
                                  context_instance=RequestContext(request))
    return render_to_response('user_management/messages.html', context_instance=RequestContext(request))


def message_form(request):
    if 'message' in request.GET:
        message = UserMessages.objects.get(id=request.GET['message'])
        if message.group:
            message_form = MessageForm(initial={'subject': 'RE: %s' % message.subject, 'group': message.group.name,
                                                'message': message.id, })
        else:
            message_form = MessageForm(initial={'to': message.sent_by, 'subject': 'RE: %s' % message.subject,
                                                'message': message.id, })
        return render_to_response('user_management/message_modal.html',
                                  {'message': message, 'message_form': message_form, },
                                  context_instance=RequestContext(request))
    message_form = MessageForm()
    return render_to_response('user_management/message_modal.html',
                              {'message_form': message_form, },
                              context_instance=RequestContext(request))


@login_required
def message_send(request):
    import pdb; pdb.set_trace()
    if request.is_ajax():
        try:
            form = MessageForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data['group']
                to = form.cleaned_data['to']
                reply_to = form.cleaned_data['message']
                if group:
                    # Add message to all members of group
                    for bracket in group.brackets.all():
                        if bracket.user != request.user:
                            message = UserMessages(to=bracket.user, sent_by=request.user,
                                                   subject=form.cleaned_data['subject'],
                                                   message=form.cleaned_data['body'], group=group,
                                                   reply_to=reply_to)
                            message.save()
                else:
                    message = UserMessages(to=to, sent_by=request.user, subject=form.cleaned_data['subject'],
                                           message=form.cleaned_data['body'], reply_to=reply_to)
                    message.save()
                return HttpResponse(json.dumps('Success'), content_type='application/json')
            return HttpResponse(json.dumps('Nope'), content_type='application/json')
        except:
            return HttpResponse(json.dumps('Nope'), content_type='application/json')


@login_required
def message_delete(request):
    if request.is_ajax() and request.method == 'POST':
        message = UserMessages.objects.get(id=request.POST['message'], to=request.user)
        message.delete()
        return HttpResponse(json.dumps('Success'), content_type='application/json')
