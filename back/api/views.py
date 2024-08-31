from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import auth
from .forms import UserLoginForm
from django.shortcuts import redirect
from .forms import UserRegisterForm


def index(request):
    print(request.user.is_authenticated)
    print(request.user)
    return render(request, template_name="index.html", context={"success": request.user.is_authenticated})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Регистрация успешна', 'redirect_url': '/profile'})
            else:
                return JsonResponse({'success': False, 'message': 'Ошибка аутентификации.'})
        else:
            return JsonResponse({'success': False, 'message': 'Пожалуйста, проверьте введенные данные.'})

    return JsonResponse({'success': False, 'message': 'Метод не поддерживается.'})


def loginu(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(form.data)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("User authenticated and logged in.")
                return JsonResponse({'success': True, 'redirect_url': '/'})
            else:
                print("Authentication failed.")
                return JsonResponse({'success': False, 'message': 'Неверное имя пользователя или пароль.'})
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'success': False, 'message': 'Пожалуйста, проверьте введенные данные.'})

    print("Method not supported.")
    return JsonResponse({'success': False, 'message': 'Метод не поддерживается.'})


def logout(request):
    auth.logout(request)
    return redirect("/")


def profile(request):
    return render(request, 'personal-account-3.html')


def createblog(request):
    return render(request, "personal-account-5.html")
