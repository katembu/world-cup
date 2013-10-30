from tournament.models import MatchPredictions


def create_matches(user):
    #Round of 16
    for i in range(49, 57):
        match = MatchPredictions(user=user, round=16, match_number=i)
        match.save()
    #Round of 8
    for i in range(57, 61):
        match = MatchPredictions(user=user, round=8, match_number=i)
        match.save()
    #Semi-finals
    for i in range(61, 63):
        match = MatchPredictions(user=user, round=4, match_number=i)
        match.save()
    #Third Place Match
    match = MatchPredictions(user=user, round=3, match_number=63)
    match.save()
    #Final
    match = MatchPredictions(user=user, round=1, match_number=64)
    match.save()


def place_team(user, group_prediction):
    match_number = None
    if group_prediction.country.group == 'A':
        if group_prediction.position == 1:
            match_number = 49
        elif group_prediction.position == 2:
            match_number = 51
    elif group_prediction.country.group == 'B':
        if group_prediction.position == 1:
            match_number = 51
        elif group_prediction.position == 2:
            match_number = 49
    elif group_prediction.country.group == 'C':
        if group_prediction.position == 1:
            match_number = 50
        elif group_prediction.position == 2:
            match_number = 52
    elif group_prediction.country.group == 'D':
        if group_prediction.position == 1:
            match_number = 52
        elif group_prediction.position == 2:
            match_number = 50
    elif group_prediction.country.group == 'E':
        if group_prediction.position == 1:
            match_number = 53
        elif group_prediction.position == 2:
            match_number = 55
    elif group_prediction.country.group == 'F':
        if group_prediction.position == 1:
            match_number = 55
        elif group_prediction.position == 2:
            match_number = 53
    elif group_prediction.country.group == 'G':
        if group_prediction.position == 1:
            match_number = 54
        elif group_prediction.position == 2:
            match_number = 56
    elif group_prediction.country.group == 'H':
        if group_prediction.position == 1:
            match_number = 56
        elif group_prediction.position == 2:
            match_number = 54
    match = MatchPredictions.objects.get(user=user, match_number=match_number)
    if group_prediction.position == 1:
        match.home_team = group_prediction.country
        match.save()
        return '%s-%s' % (match_number, 'home')
    elif group_prediction.position == 2:
        match.away_team = group_prediction.country
        match.save()
        return '%s-%s' % (match_number, 'away')
