from django.forms import ModelForm
from .models import Task

# Create a form from a table that I created before.


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
