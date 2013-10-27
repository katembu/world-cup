from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from tournament.models import *
from tournament.helpers import place_team


def index(request):
    return render_to_response('tournament/index.html', context_instance=RequestContext(request))


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
            return HttpResponse(simplejson.dumps([bracket_placement, country.id]), mimetype='application/json')
        elif request.POST['type'] == 'remove-group':
            country = Countries.objects.get(id=request.POST['country'])
            try:
                match = MatchPredictions.objects.get(user=request.user, home_team=country)
                match.home_team = None
                match.save()
            except:
                match = MatchPredictions.objects.get(user=request.user, away_team=country)
                match.away_team = None
                match.save()
            winner = GroupPredictions.objects.get(country=country)
            winner.delete()
            return HttpResponse(simplejson.dumps([country.id]), mimetype='application/json')
