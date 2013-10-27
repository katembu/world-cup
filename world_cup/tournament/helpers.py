from tournament.models import MatchWinners


def create_matches(user):
    #Round of 16
    for i in range(49, 57):
        match = MatchWinners(user=user, round=16, match_number=i)
        match.save()
    #Round of 8
    for i in range(57, 61):
        match = MatchWinners(user=user, round=8, match_number=i)
        match.save()
    #Semi-finals
    for i in range(61, 63):
        match = MatchWinners(user=user, round=4, match_number=i)
        match.save()
    #Third Place Match
    match = MatchWinners(user=user, round=3, match_number=63)
    match.save()
    #Final
    match = MatchWinners(user=user, round=1, match_number=64)
    match.save()
