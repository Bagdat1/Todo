from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Count, Q

from main.models import Task, CustomUser


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы авторизованы!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'auth/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        bio = request.POST.get('bio')

        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')
        
        if len(password) < 8:
            messages.error(request, 'Пароль должен содержать не менее 8 символов.')
            return redirect('register')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('register')
    
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            image=image,
            bio=bio
        )
        user.save()
        messages.success(request, 'Вы успешно зарегистрированы!')
        return redirect('login')
    return render(request, 'auth/register.html')


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы вышли из системы!')
        return redirect('login')
    return render(request, 'auth/logout.html')


@login_required(login_url='login')
def user_profile(request):
    profile = request.user
    completed_count = Task.objects.filter(user=profile, completed=True).count()
    uncompleted_count = Task.objects.filter(user=profile, completed=False).count()
    
    context = {
        'profile': profile,
        'completed_count': completed_count,
        'uncompleted_count': uncompleted_count
    }
    return render(request, 'auth/profile.html', context)


@login_required(login_url='login')
def user_edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        bio = request.POST.get('bio')

        if CustomUser.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('edit_profile')

        if CustomUser.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('edit_profile')

        user = request.user
        user.username = username
        user.email = email
        if image:
            user.image = image
        user.bio = bio
        user.save()
        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('profile')
    return render(request, 'auth/edit_profile.html')


@login_required(login_url='login')
def user_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('new_password_confirm')

        if new_password != new_password_confirm:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('change_password')
        
        if len(new_password) < 8:
            messages.error(request, 'Пароль должен содержать не менее 8 символов.')
            return redirect('change_password')
        
        user = authenticate(request, username=request.user.username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('login')
        else:
            messages.error(request, 'Неверный старый пароль.')
    return render(request, 'auth/change_password.html')


@login_required(login_url='login')
def todo(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo.html', {'tasks': tasks})


@login_required(login_url='login')
def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            Task.objects.create(
                title=title, 
                description=description,
                user=request.user
            )
        return redirect('todo_list')
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo.html', {'tasks': tasks})


@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(
            title=title, 
            description=description,
            user=request.user
        )
        return redirect('todo_list')
    return render(request, 'add_task.html')


@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('todo_list')
    return render(request, 'edit_task.html', {'task': task})


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('todo_list')
    return render(request, 'delete_task.html', {'task': task})


@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('todo_list')

