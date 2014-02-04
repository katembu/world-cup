from django import template
from tournament.models import Countries, GroupPredictions, MatchPredictions, Matches
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlquote

register = template.Library()


@register.filter
def group_name(group):
    return group[0].group


@register.filter
def selected_class(country, bracket):
    try:
        winner = GroupPredictions.objects.get(bracket=bracket, country=country)
        if winner.position == 1:
            return 'success'
        if winner.position == 2:
            return 'warning'
    except ObjectDoesNotExist:
        winners = GroupPredictions.objects.filter(bracket=bracket,
                                                  country__in=Countries.objects.filter(group=country.group))
        if len(winners) == 2:
            return 'active'


@register.filter
def get_match(matches, match_number):
    return matches.get(match_number=match_number)


@register.filter
def group_not_completed(bracket):
    predictions = GroupPredictions.objects.filter(bracket=bracket)
    return len(predictions) != 16


@register.filter
def score(bracket):
    bracket_score = 0
    group_predictions = GroupPredictions.objects.filter(bracket=bracket)
    for prediction in group_predictions:
        if prediction.position == prediction.country.final_position:
            bracket_score += 10
    match_predictions = MatchPredictions.objects.filter(bracket=bracket)
    for prediction in match_predictions:
        try:
            match = Matches.objects.get(match_number=prediction.match_number)
            if prediction.winner == match.winner:
                if prediction.round == 16:
                    bracket_score += 20
                elif prediction.round == 8:
                    bracket_score += 30
                elif prediction.round == 4:
                    bracket_score += 50
                elif prediction.round == 1:
                    bracket_score += 100
        except ObjectDoesNotExist:
            pass
    return bracket_score


@register.filter
def get_url(bracket):
    return 'http://soccer.ericsaupe.com/?user=%s&bracket-name=%s' % (bracket.user.username, urlquote(bracket.name))


@register.filter
def get_group_url(group):
    return 'http://soccer.ericsaupe.com/tournament/groups/%s' % urlquote(group.name)