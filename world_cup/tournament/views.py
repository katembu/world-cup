from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from django.db.models import Q
from tournament.models import *
from tournament.forms import CompetitiveGroupForm, BracketSelectForm, GroupLoginForm
from tournament.helpers import place_team, update_matches, create_matches


@login_required
def index(request):
    """
    Basic render of the tournament index page.  Used to create a new bracket with a unique name.
    Bracket names are unique to the user.
    """
    if request.method == "POST":
        try:
            bracket = Brackets.objects.get(user=request.user, name=request.POST['name'])
        except:
            create_matches(request.user, request.POST['name'])
            return redirect('/tournament/brackets/%s/' % request.POST['name'])
    return render_to_response('tournament/index.html', context_instance=RequestContext(request))


@login_required
def brackets(request, bracket_name=None):
    """
    Renders the bracket for the user.
    """
    if 'user' in request.GET and 'bracket-name' in request.GET:
        # Read-only bracket
        user = User.objects.get(username=request.GET['user'])
        bracket_name = request.GET['bracket-name']
        bracket = Brackets.objects.get(user=user, name=bracket_name)
        group_labels = Countries.objects.values('group').distinct()
        groups = []
        for label in group_labels:
            label = label['group']
            groups.append(Countries.objects.filter(group=label))
        matches = MatchPredictions.objects.filter(bracket=bracket)
        return render_to_response('tournament/brackets.html',
                                  {'bracket': bracket, 'groups': groups, 'matches': matches,
                                   'read_only': True, },
                                  context_instance=RequestContext(request))
    if not bracket_name:
        # List all brackets for user
        brackets = Brackets.objects.filter(user=request.user)
        return render_to_response('tournament/brackets_list.html', {'brackets': brackets, },
                                  context_instance=RequestContext(request))
    # Render user bracket
    bracket = Brackets.objects.get(user=request.user, name=bracket_name)
    group_labels = Countries.objects.values('group').distinct()
    groups = []
    for label in group_labels:
        label = label['group']
        groups.append(Countries.objects.filter(group=label))
    matches = MatchPredictions.objects.filter(bracket=bracket)
    return render_to_response('tournament/brackets.html',
                              {'bracket': bracket, 'groups': groups, 'matches': matches, 'read_only': False, },
                              context_instance=RequestContext(request))


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
            return HttpResponse(simplejson.dumps([bracket_placement, country.id, country.name]),
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
            return HttpResponse(simplejson.dumps([output, country.id, country.name]), mimetype='application/json')
        #Called when a knockout round selection is made.
        elif request.POST['type'] == 'save-match':
            bracket = Brackets.objects.get(user=request.user, name=request.POST['bracket'])
            match = MatchPredictions.objects.get(bracket=bracket, match_number=request.POST['match_number'])
            if request.POST['home_away'] == 'home':
                winner = match.home_team
            elif request.POST['home_away'] == 'away':
                winner = match.away_team
            match.winner = winner
            match.save()
            output = update_matches(request.user, bracket.name, match)
            return HttpResponse(simplejson.dumps([output, winner.id, winner.name]), mimetype='application/json')


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
        group = CompetitiveGroups.objects.get(name=group_name)
        # Save bracket to group if request is POST
        if request.method == 'POST':
            bracket_form = BracketSelectForm(request.POST)
            if bracket_form.is_valid():
                group.brackets.add(bracket_form.cleaned_data['brackets'])
        # Check if user is in the group or has permission to be here
        user_in_group = group.brackets.filter(user=request.user)
        user_has_permission = GroupPermissions.objects.filter(user=request.user, group=group, allowed=True)
        # If they don't, and we require a password, redirect to group login view
        if group.password and not (user_in_group or user_has_permission):
            return redirect('/tournament/login/%s/' % group.name)
        # Render page with bracket selection, may not be used if user already in group
        bracket_form = BracketSelectForm()
        bracket_form.fields['brackets'].queryset = Brackets.objects.filter(user=request.user)
        return render_to_response('tournament/group_page.html', {'group': group, 'bracket_form': bracket_form,
                                                                 'user_in_group': user_in_group, },
                                  context_instance=RequestContext(request))
    else:
        # Render user group list and group creation form
        groups = CompetitiveGroups.objects.filter(brackets__user=request.user)
        public_groups = CompetitiveGroups.objects.filter(password='')
        # Save group form
        if request.method == 'POST':
            form = CompetitiveGroupForm(request.POST)
            if form.is_valid():
                new_group = form.save(commit=False)
                new_group.creator = request.user
                new_group.save()
                new_group.brackets.add(form.cleaned_data['brackets'])
                return redirect('/tournament/groups/%s/' % new_group.name)
            else:
                form.fields['brackets'].queryset = Brackets.objects.filter(user=request.user)
                return render_to_response('tournament/groups.html', {'form': form, 'groups': groups,
                                                                     'public_groups': public_groups, },
                                          context_instance=RequestContext(request))
        # Render page and group form
        form = CompetitiveGroupForm()
        form.fields['brackets'].queryset = Brackets.objects.filter(user=request.user)
        return render_to_response('tournament/groups.html', {'form': form, 'groups': groups,
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
                return redirect('/tournament/groups/%s/' % group.name)
    return render_to_response('tournament/group_login.html', {'form': form, 'group': group, },
                              context_instance=RequestContext(request))
