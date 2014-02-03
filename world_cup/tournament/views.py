from django.http import *
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, Context
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.db.models import Q
from django.utils.http import urlquote
from tournament.models import *
from tournament.forms import CompetitiveGroupForm, BracketSelectForm, GroupLoginForm
from tournament.helpers import place_team, update_matches, create_matches
from user_management.models import CustomUser as User
from user_management.forms import MessageForm
from world_cup.helpers import EmailThread
from django.core.exceptions import ObjectDoesNotExist
import json


def brackets(request):
    """
    Renders the bracket for the user.
    """
    if 'user' in request.GET and 'bracket-name' in request.GET:
        # Read-only bracket
        user = User.objects.get(username=request.GET['user'])
        bracket_name = request.GET['bracket-name']
        bracket = Brackets.objects.get(user=user, name=bracket_name)
        group_labels = Countries.objects.values('group').distinct()
        group_predictions = []
        for label in group_labels:
            label = label['group']
            group_predictions.append(Countries.objects.filter(group=label))
        matches = MatchPredictions.objects.filter(bracket=bracket)
        return render_to_response('tournament/brackets.html',
                                  {'bracket': bracket, 'groups': group_predictions, 'matches': matches,
                                   'read_only': True, },
                                  context_instance=RequestContext(request))
    if request.user.is_authenticated():
        # List all brackets for user
        user_brackets = Brackets.objects.filter(user=request.user)
        if request.method == "POST":
            try:
                Brackets.objects.get(user=request.user, name=request.POST['name'])
            except ObjectDoesNotExist:
                create_matches(request.user, request.POST['name'])
                return redirect(urlquote('/tournament/brackets/%s/' % request.POST['name']))
        return render_to_response('tournament/brackets_list.html', {'brackets': user_brackets, },
                                  context_instance=RequestContext(request))
    return redirect('/accounts/login/?next=/tournament/brackets/')


@login_required
def render_bracket(request, bracket_name):
    # Render user bracket
    bracket = get_object_or_404(Brackets, user=request.user, name=bracket_name)
    # Change name
    if request.method == 'POST':
        bracket.name = request.POST['bracket-name']
        bracket.save()
        return redirect(urlquote('/tournament/brackets/%s/' % bracket.name))
    group_labels = Countries.objects.values('group').distinct()
    group_predictions = []
    for label in group_labels:
        label = label['group']
        group_predictions.append(Countries.objects.filter(group=label))
    matches = MatchPredictions.objects.filter(bracket=bracket)
    return render_to_response('tournament/brackets.html',
                              {'bracket': bracket, 'groups': group_predictions, 'matches': matches,
                               'read_only': False, },
                              context_instance=RequestContext(request))


@login_required
def save(request):
    """
    Saves a selection for the user.  Has various checks and will return errors if any are encountered.
    """
    if request.method == 'POST':
        #Called when a group selection is made.
        if request.POST['type'] == 'add-group':
            country = Countries.objects.get(id=request.POST['country'])
            position = int(request.POST['position'])
            bracket = Brackets.objects.get(user=request.user, name=request.POST['bracket'])
            winner = GroupPredictions(bracket=bracket, country=country, position=position)
            winner.save()
            bracket_placement = place_team(request.user, bracket.name, winner)
            return HttpResponse(json.dumps([bracket_placement, country.id, country.name]),
                                mimetype='application/json')
        #Called when a group selection is unselected.
        elif request.POST['type'] == 'remove-group':
            country = Countries.objects.get(id=request.POST['country'])
            bracket = Brackets.objects.get(user=request.user, name=request.POST['bracket'])
            matches = MatchPredictions.objects.filter(Q(home_team=country) | Q(away_team=country), bracket=bracket)
            output = []
            for match in matches:
                if match.home_team == country:
                    match.home_team = None
                    output.append('%s-%s' % (match.match_number, 'home'))
                elif match.away_team == country:
                    match.away_team = None
                    output.append('%s-%s' % (match.match_number, 'away'))
                match.save()
            winner = GroupPredictions.objects.get(bracket=bracket, country=country)
            winner.delete()
            return HttpResponse(json.dumps([output, country.id, country.name]), mimetype='application/json')
        #Called when a knockout round selection is made.
        elif request.POST['type'] == 'save-match':
            bracket = Brackets.objects.get(user=request.user, name=request.POST['bracket'])
            match = MatchPredictions.objects.get(bracket=bracket, match_number=request.POST['match_number'])
            winner = None
            if request.POST['home_away'] == 'home':
                winner = match.home_team
            elif request.POST['home_away'] == 'away':
                winner = match.away_team
            match.winner = winner
            match.save()
            output = update_matches(request.user, bracket.name, match)
            return HttpResponse(json.dumps([output, winner.id, winner.name]), mimetype='application/json')


@login_required
def delete(request):
    if request.method == 'POST':
        bracket = Brackets.objects.get(user=request.user, name=request.POST['bracket'])
        bracket.delete()
        return HttpResponse(json.dumps('Success'), mimetype='application/json')


@login_required
def reset(request):
    if 'bracket' in request.POST:
        bracket = Brackets.objects.get(user=request.user, name=request.POST['bracket'])
        matches = MatchPredictions.objects.filter(bracket=bracket)
        for match in matches:
            match.home_team = None
            match.away_team = None
            match.winner = None
            match.save()
        group_predictions = GroupPredictions.objects.filter(bracket=bracket)
        for prediction in group_predictions:
            prediction.delete()
        return HttpResponse(json.dumps('Success'), mimetype='application/json')


def about(request):
    """
    Basic render of the about page to inform about the World Cup and what this site is about.
    """
    return render_to_response('tournament/about.html', context_instance=RequestContext(request))


@login_required
def groups(request, group_name=None):
    """
    Groups method renders a group page if a group name is given.  If not, a group creation/list page is rendered.
    """
    if group_name:
        # Get Group
        group = get_object_or_404(CompetitiveGroups, name=group_name)
        # Save bracket to group if request is POST
        if request.method == 'POST':
            bracket_form = BracketSelectForm(request.POST)
            if bracket_form.is_valid():
                try:
                    bracket = Brackets.objects.get(user=request.user, competitivegroups=group)
                    group.brackets.remove(bracket)
                except ObjectDoesNotExist:
                    pass
                group.brackets.add(bracket_form.cleaned_data['brackets'])
        # Check if user is in the group or has permission to be here
        user_in_group = group.brackets.filter(user=request.user)
        user_has_permission = GroupPermissions.objects.filter(user=request.user, group=group, allowed=True)
        # If they don't, and we require a password, redirect to group login view
        if group.password and not (user_in_group or user_has_permission):
            return redirect(urlquote('/tournament/login/%s/' % group.name))
        # Render page with bracket selection, may not be used if user already in group
        bracket_form = BracketSelectForm()
        bracket_form.fields['brackets'].queryset = Brackets.objects.filter(user=request.user)
        message_form = MessageForm()
        return render_to_response('tournament/group_page.html', {'group': group, 'bracket_form': bracket_form,
                                                                 'message_form': message_form,
                                                                 'user_in_group': user_in_group, },
                                  context_instance=RequestContext(request))
    else:
        # Render user group list and group creation form
        competitive_groups = CompetitiveGroups.objects.filter(brackets__user=request.user)
        public_groups = CompetitiveGroups.objects.filter(password='')
        # Save group form
        if request.method == 'POST':
            form = CompetitiveGroupForm(request.POST)
            if form.is_valid():
                new_group = form.save(commit=False)
                new_group.creator = request.user
                new_group.save()
                new_group.brackets.add(form.cleaned_data['brackets'])
                return redirect(urlquote('/tournament/groups/%s/' % new_group.name))
            else:
                form.fields['brackets'].queryset = Brackets.objects.filter(user=request.user)
                return render_to_response('tournament/groups.html', {'form': form, 'groups': competitive_groups,
                                                                     'public_groups': public_groups, },
                                          context_instance=RequestContext(request))
        # Render page and group form
        form = CompetitiveGroupForm()
        form.fields['brackets'].queryset = Brackets.objects.filter(user=request.user)
        return render_to_response('tournament/groups.html', {'form': form, 'groups': competitive_groups,
                                                             'public_groups': public_groups, },
                                  context_instance=RequestContext(request))


@login_required
def group_login(request, group_name):
    """
    Group login page is used when a user encounters a group they are not part of that is password protected.
    """
    group = CompetitiveGroups.objects.get(name=group_name)
    form = GroupLoginForm()
    if request.method == 'POST':
        form = GroupLoginForm(request.POST)
        if form.is_valid():
            # Verify password is the same as the group
            if form.cleaned_data['password'] == group.password:
                # Add user to group permissions
                permission = GroupPermissions(user=request.user, group=group, allowed=True)
                permission.save()
                return redirect(urlquote('/tournament/groups/%s/' % group.name))
    return render_to_response('tournament/group_login.html', {'form': form, 'group': group, },
                              context_instance=RequestContext(request))


@login_required
def send_invites(request, group_name):
    if request.method == 'POST':
        group = CompetitiveGroups.objects.get(name=group_name)
        to = request.POST.getlist('invites[]')
        email_addresses = []
        for address in to:
            if '@' in address:
                email_addresses.append(address)
            else:
                try:
                    user = User.objects.get(username=address)
                    email_addresses.append(user.email)
                except ObjectDoesNotExist:
                    pass
        subject = '%s wants you in %s | %s' % (request.user, group.name, 'soccer.ericsaupe.com')
        content = '%s wants you to join the group \
                  <a href="http://soccer.ericsaupe.com/tournament/groups/%s">%s</a>.<br/> \
                  Prove you can predict the World Cup better than them!' % (request.user, urlquote(group.name),
                                                                            group.name)
        if group.password:
            content += 'This is a private group.  To get in you will need the password below. <br/>\
                       <strong>Password:</strong> %s' % group.password
        template = get_template('user_management/message_email.html')
        context = Context({'header': subject, 'content': content, 'user': request.user, 'footer': False})
        body = template.render(context)
        EmailThread(subject, body, email_addresses).start()
        return HttpResponse(json.dumps('Success'), mimetype='application/json')


@login_required
def leave_group(request):
    if 'group' in request.POST:
        group = CompetitiveGroups.objects.get(id=request.POST['group'])
        bracket = Brackets.objects.get(user=request.user, competitivegroups=group)
        group.brackets.remove(bracket)
        if len(group.brackets.all()) == 0:
            group.delete()
        return HttpResponse(json.dumps('Success'), mimetype='application/json')


def usa(request):
    return render_to_response('tournament/usa.html', context_instance=RequestContext(request))