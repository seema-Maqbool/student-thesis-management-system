from django.contrib import admin
from .models import Thesis, Profile


@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'student_name', 'supervisor_name', 'department', 'university', 'created_at')
    search_fields = ('title', 'student_name', 'supervisor_name', 'department', 'university')
    list_filter = ('department', 'university')


admin.site.register(Profile)