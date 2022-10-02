from django.contrib import admin
from .models import Task
# Register your models here.
#With this I can see the Task table in the admin panel

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


admin.site.register(Task, TaskAdmin)