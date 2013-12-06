from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from django.db.models import Q
from tournament.models import *
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
    if not bracket_name:
        brackets = Brackets.objects.filter(user=request.user)
        return render_to_response('tournament/brackets_list.html', {'brackets': brackets, },
                                  context_instance=RequestContext(request))
    bracket = Brackets.objects.get(user=request.user, name=bracket_name)
    group_labels = Countries.objects.values('group').distinct()
    groups = []
    for label in group_labels:
        label = label['group']
        groups.append(Countries.objects.filter(group=label))
    matches = MatchPredictions.objects.filter(bracket=bracket)
    return render_to_response('tournament/brackets.html', {'bracket': bracket, 'groups': groups, 'matches': matches},
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
            winner = GroupPredictions.objects.get(country=country)
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
