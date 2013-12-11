from tournament.models import MatchPredictions, Brackets


def create_matches(user, bracket_name):
    bracket = Brackets(user=user, name=bracket_name)
    bracket.save()
    #Round of 16
    for i in range(49, 57):
        match = MatchPredictions(bracket=bracket, round=16, match_number=i)
        match.save()
    #Round of 8
    for i in range(57, 61):
        match = MatchPredictions(bracket=bracket, round=8, match_number=i)
        match.save()
    #Semi-finals
    for i in range(61, 63):
        match = MatchPredictions(bracket=bracket, round=4, match_number=i)
        match.save()
    #Third Place Match
    match = MatchPredictions(bracket=bracket, round=3, match_number=63)
    match.save()
    #Final
    match = MatchPredictions(bracket=bracket, round=1, match_number=64)
    match.save()


def place_team(user, bracket_name, group_prediction):
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
    bracket = Brackets.objects.get(user=user, name=bracket_name)
    match = MatchPredictions.objects.get(bracket=bracket, match_number=match_number)
    if group_prediction.position == 1:
        match.home_team = group_prediction.country
        match.save()
        return '%s-%s' % (match_number, 'home')
    elif group_prediction.position == 2:
        match.away_team = group_prediction.country
        match.save()
        return '%s-%s' % (match_number, 'away')


def update_matches(user, bracket_name, match):
    bracket = Brackets.objects.get(user=user, name=bracket_name)
    if match.match_number == 49:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=57)
        next_match.home_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 50:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=57)
        next_match.away_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
    elif match.match_number == 51:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=59)
        next_match.home_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 52:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=59)
        next_match.away_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
    elif match.match_number == 53:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=58)
        next_match.home_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 54:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=58)
        next_match.away_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
    elif match.match_number == 55:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=60)
        next_match.home_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 56:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=60)
        next_match.away_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
    elif match.match_number == 57:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=61)
        next_match.home_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 58:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=61)
        next_match.away_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
    elif match.match_number == 59:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=62)
        next_match.home_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 60:
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=62)
        next_match.away_team = match.winner
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
    elif match.match_number == 61:
        #Final
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=64)
        next_match.home_team = match.winner
        #Third Place
        third_place = MatchPredictions.objects.get(bracket=bracket, match_number=63)
        if match.home_team == match.winner:
            third_place.home_team = match.away_team
        else:
            third_place.home_team = match.home_team
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'home')
    elif match.match_number == 62:
        #Final
        next_match = MatchPredictions.objects.get(bracket=bracket, match_number=64)
        next_match.away_team = match.winner
        #Third Place
        third_place = MatchPredictions.objects.get(bracket=bracket, match_number=63)
        if match.home_team == match.winner:
            third_place.away_team = match.away_team
        else:
            third_place.away_team = match.home_team
        next_match.save()
        return '%s-%s' % (next_match.match_number, 'away')
