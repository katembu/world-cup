from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from django.db.models import Q
from tournament.models import *
from tournament.helpers import place_team, update_matches


def index(request):
    return render_to_response('tournament/index.html', context_instance=RequestContext(request))


@login_required
def brackets(request):
    group_labels = Countries.objects.values('group').distinct()
    groups = []
    for label in group_labels:
        label = label['group']
        groups.append(Countries.objects.filter(group=label))
    matches = MatchPredictions.objects.filter(user=request.user)
    return render_to_response('tournament/brackets.html', {'groups': groups, 'matches': matches},
                              context_instance=RequestContext(request))


def save(request):
    if request.method == 'POST':
        if request.POST['type'] == 'add-group':
            country = Countries.objects.get(id=request.POST['country'])
            position = int(request.POST['position'])
            winner = GroupPredictions(user=request.user, country=country, position=position)
            winner.save()
            bracket_placement = place_team(request.user, winner)
            return HttpResponse(simplejson.dumps([bracket_placement, country.id, country.name]),
                                mimetype='application/json')
        elif request.POST['type'] == 'remove-group':
            country = Countries.objects.get(id=request.POST['country'])
            matches = MatchPredictions.objects.filter(Q(home_team=country) | Q(away_team=country), user=request.user)
            output = []
            for match in matches:
                if match.home_team == country:
                    match.home_team = None
                    output.append('%s-%s' % (match.match_number, 'home'))
                elif match.away_team == countr:
                    match.away_team = None
                    output.append('%s-%s' % (match.match_number, 'away'))
                match.save()
            winner = GroupPredictions.objects.get(country=country)
            winner.delete()
            return HttpResponse(simplejson.dumps([output, country.id, country.name]), mimetype='application/json')
        elif request.POST['type'] == 'save-match':
            match = MatchPredictions.objects.get(user=request.user, match_number=request.POST['match_number'])
            if request.POST['home_away'] == 'home':
                winner = match.home_team
            elif request.POST['home_away'] == 'away':
                winner = match.away_team
            match.winner = winner
            match.save()
            output = update_matches(request.user, match)
            return HttpResponse(simplejson.dumps([output, winner.id, winner.name]), mimetype='application/json')
