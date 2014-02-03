from django.http import *
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from user_management.forms import *
from user_management.models import UserMessages
from user_management.models import CustomUser as User
from tournament.helpers import create_matches
from world_cup.helpers import EmailThread
import json


def login_user(request):
    """
    Logs in the user and redirects them if they tried to access a page that requires login.
    """
    logout(request)
    username = password = ''
    user = None
    next = request.GET['next'] if 'next' in request.GET else None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
            return HttpResponseRedirect('%s' % next if next != 'None' else '/')
        return render_to_response('login.html', {'next': next, 'error': True, 'username':username},
                                  context_instance=RequestContext(request))
    return render_to_response('login.html', {'next': next, 'error': False}, context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect('user_management.views.index')


def create_user(request):
    """
    Creates user and redirects to home page.
    """
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


@login_required
def messages(request):
    """
    Renders the user's messages or a single message if the id parameter is in the request.
    """
    if 'id' in request.GET:
        try:
            message = UserMessages.objects.get(id=request.GET['id'], to=request.user)
            message.read = True
            message.save()
            return render_to_response('user_management/messages.html', {'message': message, },
                                      context_instance=RequestContext(request))
        except:
            pass
    return render_to_response('user_management/messages.html', context_instance=RequestContext(request))


@login_required
def message_form(request):
    """
    Message form to be rendered in a Bootstrap modal.
    """
    if 'group' in request.GET:
        group = CompetitiveGroups.objects.get(id=request.GET['group'])
        message_form = MessageForm(initial={'group': group.name, })
    elif 'message' in request.GET:
        message = UserMessages.objects.get(id=request.GET['message'], to=request.user)
        if message.group:
            message_form = MessageForm(initial={'subject': 'RE: %s' % message.subject, 'group': message.group.name,
                                                'message': message.id, })
        else:
            message_form = MessageForm(initial={'to': message.sent_by, 'subject': 'RE: %s' % message.subject,
                                                'message': message.id, })
        return render_to_response('user_management/message_modal.html',
                                  {'message': message, 'message_form': message_form, },
                                  context_instance=RequestContext(request))
    else:
        message_form = MessageForm()
    return render_to_response('user_management/message_modal.html',
                              {'message_form': message_form, },
                              context_instance=RequestContext(request))


@login_required
def message_send(request):
    """
    Sends messages to recipients and notifies them by email if that setting is true.
    """
    if request.is_ajax():
        try:
            form = MessageForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data['group']
                to = form.cleaned_data['to']
                reply_to = form.cleaned_data['message']
                subject = '%s - %s | %s' % (request.user, form.cleaned_data['subject'], 'soccer.ericsaupe.com')
                content = '%s sent you a message at %s.<br/>Check out your \
                <a href="http://%s/messages/">messages</a> to read it.' % (request.user, 'soccer.ericsaupe.com',
                                                                           'soccer.ericsaupe.com')
                template = get_template('user_management/message_email.html')
                context = Context({'header': subject, 'content': content, 'user': request.user, 'footer': True})
                body = template.render(context)
                if group:
                    # Add message to all members of group
                    for bracket in group.brackets.all():
                        if bracket.user != request.user:
                            message = UserMessages(to=bracket.user, sent_by=request.user,
                                                   subject=form.cleaned_data['subject'],
                                                   message=form.cleaned_data['body'], group=group,
                                                   reply_to=reply_to)
                            message.save()
                            if bracket.user.message_notifications:
                                EmailThread(subject, body, [bracket.user.email, ]).start()
                else:
                    message = UserMessages(to=to, sent_by=request.user, subject=form.cleaned_data['subject'],
                                           message=form.cleaned_data['body'], reply_to=reply_to)
                    message.save()
                    if to.message_notifications:
                        EmailThread(subject, body, [to.email, ]).start()
                return HttpResponse(json.dumps('Success'), content_type='application/json')
            return HttpResponse(json.dumps('Nope'), content_type='application/json')
        except:
            return HttpResponse(json.dumps('Nope'), content_type='application/json')


@login_required
def message_delete(request):
    """
    Deletes user message.
    """
    if request.is_ajax() and request.method == 'POST':
        message = UserMessages.objects.get(id=request.POST['message'], to=request.user)
        message.delete()
        return HttpResponse(json.dumps('Success'), content_type='application/json')


@login_required
def user_list(request):
    """
    Returns list of users that want to be searchable for messaging.
    """
    output = []
    users = User.objects.filter(searchable=True)
    for user in users:
        output.append({'value': '%s' % user.username,
                       'tokens': user.username.split(),
                       'image': user.image.url if user.image else 'http://www.regentsprep.org/regents/math/geometry/GG2/soccerball.jpg'})
    return HttpResponse(json.dumps(output), content_type='application/json')


@login_required
def user_profile(request):
    """
    Renders the user's profile.
    """
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            password = profile_form.cleaned_data['password1']
            if password:
                request.user.set_password(password)
                request.user.save()
            profile_form.save()
        else:
            return render_to_response('user_management/profile.html', {'form': profile_form, },
                                      context_instance=RequestContext(request))
    profile_form = UserProfileForm(initial=({'first_name': request.user.first_name,
                                             'last_name': request.user.last_name,
                                             'email': request.user.email,
                                             'language': request.user.language,
                                             'newsletter': request.user.newsletter,
                                             'message_notifications': request.user.message_notifications,
                                             'searchable': request.user.searchable,
                                             'show_full_name': request.user.show_full_name}))
    return render_to_response('user_management/profile.html', {'form': profile_form, },
                              context_instance=RequestContext(request))


def unsubscribe(request):
    """
    Unsubscribes the given username from receiving message notifications via email.
    """
    user = get_object_or_404(User, username=request.GET['user'])
    user.message_notifications = False
    user.save()
    return render_to_response('user_management/unsubscribe.html', {'user': user, },
                              context_instance=RequestContext(request))
