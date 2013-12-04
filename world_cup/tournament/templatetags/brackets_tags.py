from django import template
from tournament.models import Countries, GroupPredictions

register = template.Library()


@register.filter
def group_name(group):
    return group[0].group


@register.filter
def selected_class(country, bracket_name):
    try:
        winner = GroupPredictions.objects.get(bracket__name=bracket_name, country=country)
        if winner.position == 1:
            return 'success'
        if winner.position == 2:
            return 'warning'
    except:
        winners = GroupPredictions.objects.filter(bracket__name=bracket_name, country__in=Countries.objects.filter(group=country.group))
        if len(winners) == 2:
            return 'active'


@register.filter
def get_match(matches, match_number):
    return matches.get(match_number=match_number)
