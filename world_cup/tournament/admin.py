from django.contrib import admin
from tournament.models import Countries, Brackets, GroupPredictions, MatchPredictions, Matches

class BracketsAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')
admin.site.register(Brackets, BracketsAdmin)

class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'position')
admin.site.register(Countries, CountriesAdmin)


class GroupPredictionsAdmin(admin.ModelAdmin):
    list_display = ('bracket', 'country', 'position')
admin.site.register(GroupPredictions, GroupPredictionsAdmin)


class MatchesAdmin(admin.ModelAdmin):
    list_display = ('round', 'winner', 'match_number')
admin.site.register(Matches, MatchesAdmin)
