from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseBadRequest, QueryDict
from django.shortcuts import render
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from back import settings
from .forms import UserLoginForm, UserProfileForm
from django.shortcuts import redirect
from .forms import UserRegisterForm
from .models import Reklama, ApiUser, Service, Category


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправление на страницу входа, если пользователь не авторизован

        user = request.user
        data_joined = user.date_joined.strftime('%d.%m.%Y')
        descr = request.user.descr

        form = UserProfileForm(initial={
            'user_name': user.username,
            'user_about': user.photo,
        })

        # Передаем URL фото пользователя, если оно есть, иначе URL по умолчанию
        photo_url = user.photo.url if user.photo else 'https://protraffic.com/wp-content/themes/ptf/images/user.svg'

        return render(request, 'profile_main.html', {
            'form': form,
            'data_joined': data_joined,
            'user': user,
            'photo_url': photo_url,
            'descr': descr,
        })

    @method_decorator(csrf_exempt)
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            user_about = form.cleaned_data.get('user_about')
            user_ava_img = form.cleaned_data.get('user_ava_img')

            user = request.user
            user.username = user_name
            user.descr = user_about
            if user_ava_img:
                user.photo = user_ava_img
            user.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})


def services(request):
    services = {i: {i1 for i1 in Service.objects.all().filter(category=i)} for i in Category.objects.all()}
    services_prepared = []
    for outer_key, inner_dict in services.items():
        services_prepared.append({
            'outer_key': outer_key,
            'inner_dict': inner_dict
        })
    print(services.items())
    return render(request, "services.html", context={"services": services_prepared})



def services_add(request):
    page = int(request.GET.get('page', 1))
    services_per_page = 2
    start = (page - 1) * services_per_page
    end = start + services_per_page
    print(start, end)

    # Рассчитываем начало и конец выборки

    # Получаем сервисы для текущей страницы
    services_data = []
    services = Service.objects.all()[start:end]

    for service in services:
        services_data.append({
            'id': service.id,
            'descr': service.descr,
            'photo': service.photo.url,
            'website': service.website,
            'promo': service.promo,
            'costs': service.costs,
        })

    return JsonResponse(services_data, safe=False)


def index(request):
    print(request.user.is_authenticated)
    print(request.user)
    photo = False
    url = False
    if Reklama.objects.filter(pos_reklama="1").exists():
        url = Reklama.objects.get(pos_reklama="1").url
        photo = Reklama.objects.get(pos_reklama="1").photo

    return render(request,
                  template_name="index.html",
                  context={"image": photo, "url_image": url,
                           "success": request.user.is_authenticated,
                           'MEDIA_URL': settings.MEDIA_URL})


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


def createblog(request):
    return render(request, "personal-account-5.html")
