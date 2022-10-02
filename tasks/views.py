from turtle import undo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

from tasks.models import Task
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    # Render to open a HTML file
    return render(request, "home.html")


def signup(request):

    if request.method == 'GET':
        print("enviando...")
        return render(request, "signup.html", {
            'form': UserCreationForm,
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    'form': UserCreationForm,
                    'error': 'User already exists',
                })
        return render(request, "signup.html", {
            'form': UserCreationForm,
            'error': "Password don't match"
        })

@login_required
def tasks(request):
    # Interact with the DataBase to do a Query
    # This return all the elements in the table TASK that are relationate with the user logged.
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    done_tasks = Task.objects.filter(user=request.user, datecompleted__isnull = False)

    return render(request, "tasks.html", {
        'tasks': tasks,
        'done_tasks': done_tasks,
    })

@login_required
def create_task(request):

    if request.method == 'GET':

        return render(request, "create_task.html", {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()

            return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html", {
                'form': TaskForm,
                'error': "An error has been ocurred",
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # If I have an error with this method, all the server will down
        #task = Task.objects.get(pk=task_id)
        # First paramter, the MODEl, second parameter the Primary Key to search the object
        task = get_object_or_404(Task, pk=task_id)

        form = TaskForm(instance=task)

        return render(request, "task_detail.html", {
            'task': task,
            'form': form,
        })

    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, "task_detail.html", {
                'task': task,
                'form': form,
                'error': 'Error'
            })

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
@login_required
def signout(request):
    logout(request)

    return redirect("home")


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "User or password is incorrect"
            })
        else:
            login(request, user)
            return redirect('tasks')


