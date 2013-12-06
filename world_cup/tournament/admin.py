from django.contrib import admin
from tournament.models import Countries, Brackets

admin.site.register(Brackets)


class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'position')
admin.site.register(Countries, CountriesAdmin)
