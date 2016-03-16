from django.contrib import admin
from application.models import Application, Vote


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'university',
                    'start_date', 'end_date', 'semester_year', 'gpa',)
    search_fields = ['email', ]


class VoteAdmin(admin.ModelAdmin):
    list_display = ('application', 'user', 'point')

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Vote, VoteAdmin)
