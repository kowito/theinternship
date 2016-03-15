from django.contrib import admin
from application.models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'university', 'semester_year', 'gpa',)

admin.site.register(Application, ApplicationAdmin)
