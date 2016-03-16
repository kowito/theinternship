from django.contrib import admin
from application.models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'university',
                    'start_date', 'end_date', 'semester_year', 'gpa',)
    search_fields = ['email', ]


admin.site.register(Application, ApplicationAdmin)
