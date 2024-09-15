from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from back import settings
from .forms import UserLoginForm, UserProfileForm
from django.shortcuts import redirect
from .forms import UserRegisterForm
from .models import Reklama, Service, Category, Obzor, Category_partner, Partner, Obzor_partner
from django.shortcuts import get_object_or_404
from .forms import ArticleForm
from django.views.generic.edit import CreateView
from .models import Article


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'personal-account-1.html')

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
            return redirect('/')

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


def partners(request):
    categories = Category_partner.objects.all()
    partners = {category: Partner.objects.filter(category_partner=category)[:5] for category in categories}

    partners_prepared = []

    for category, partners_list in partners.items():
        category_partners = []
        for partner in partners_list:
            # Try to find an Obzor object related to the current service
            obzor_id = ''
            if not partner.website:
                obzor = Obzor_partner.objects.filter(to_partner=partner).first()
                if obzor:
                    obzor_id = obzor.id

            # Prepare the service dictionary
            partners_data = {
                'id': partner.id,
                'descr': partner.descr,
                'photo': partner.photo.url,
                'website': partner.website if partner.website else f"/obzorp/{obzor_id}",
                'promo': partner.promo,
                'costs': partner.costs,
                'category': partner.category_partner,
                'ifwebsite': bool(partner.website),
                'rating': partner.rating,
            }

            category_partners.append(partners_data)

        partners_prepared.append({
            'category': category,
            'partners': category_partners,
        })
    print(partners_prepared)
    return render(request, "affiliate_program.html", context={"partners": partners_prepared})


def partner_cat(request):
    cat = int(request.GET.get('cat'))
    a = []
    query = Partner.objects.all().filter(category_partner=Category_partner.objects.all().filter(id=cat)[:1])
    for i in query:
        a.append({
            'id': i.id,
            'descr': i.descr,
            'photo': i.photo.url,
            'website': i.website if i.website else f"/obzorp/{Obzor_partner.objects.filter(to_partner=i)[0].id}",
            'promo': i.promo,
            'costs': i.costs,
            'category': i.category_partner,
            'ifwebsite': bool(i.website),
            'rating': i.rating,

        })
    return render(request, 'partners_cat.html',
                  context={"partners": a,
                           "category": Category_partner.objects.get(id=cat).perevod})


def services(request):
    # Fetch categories and services more efficiently
    categories = Category.objects.all()
    services = {category: Service.objects.filter(category=category)[:5] for category in categories}

    services_prepared = []

    for category, service_list in services.items():
        category_services = []
        for service in service_list:
            # Try to find an Obzor object related to the current service
            obzor_id = ''
            if not service.website:
                obzor = Obzor.objects.filter(to_service=service).first()
                if obzor:
                    obzor_id = obzor.id

            # Prepare the service dictionary
            service_data = {
                'id': service.id,
                'descr': service.descr,
                'photo': service.photo.url,
                'website': service.website if service.website else f"/obzor/{obzor_id}",
                'promo': service.promo,
                'costs': service.costs,
                'category': service.category,
                'ifwebsite': bool(service.website),

            }

            category_services.append(service_data)

        services_prepared.append({
            'category': category,
            'services': category_services
        })

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


def service_cat(request):
    cat = int(request.GET.get('cat'))
    a = []
    query = Service.objects.all().filter(category=Category.objects.all().filter(id=cat)[:1])
    for i in query:
        a.append({
            'id': i.id,
            'descr': i.descr,
            'photo': i.photo.url,
            'website': i.website if i.website else f"/obzor/{Obzor.objects.filter(to_service=i)[0].id}",
            'promo': i.promo,
            'costs': i.costs,
            'category': i.category,
            'ifwebsite': True if i.website else False,
        })
    return render(request, 'services_cat.html',
                  context={"services": a,
                           "category": Category.objects.get(id=cat).perevod})


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)  # Не сохраняем сразу
            article.author = request.user  # Устанавливаем текущего пользователя как автора
            article.save()  # Теперь сохраняем
            return redirect('/articles')  # Перенаправляем пользователя после создания статьи
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form})


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'create_article.html'
    success_url = '/articles'  # Замените на нужный URL


def article_list(request):
    articles = Article.objects.all()  # Извлекаем все статьи
    return render(request, 'articles.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})


def obzor_detail(request, obzor_id):
    obzor = get_object_or_404(Obzor, id=obzor_id)
    return render(request, 'obzor.html', {'obzor': obzor})


def obzorp_detail(request, obzor_id):
    obzor = get_object_or_404(Obzor_partner, id=obzor_id)
    return render(request, 'obzor.html', {'obzor': obzor})
