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
from .models import Reklama, Service, Category, Obzor, Category_partner, Partner, Obzor_partner, ApiUser
from django.shortcuts import get_object_or_404
from .forms import ArticleForm
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from .models import Article
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def index(request):
    # Получаем текущего пользователя
    user = request.user
    # Передаем пользователя в шаблон
    return render(request, 'index.html', {'user': user})

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
    # Определяем список допустимых значений для pos
    allowed_pos = ["1", "2", "3", "4", "5"]

    # Загружаем все категории партнёров
    categories = Category_partner.objects.all()

    # Фильтруем и сортируем партнёров по категории и значению pos
    partners = {
        category: Partner.objects.filter(category_partner=category, pos__in=allowed_pos).order_by('pos')[:5]
        for category in categories
    }

    partners_prepared = []

    for category, partners_list in partners.items():
        category_partners = []
        for partner in partners_list:
            # Попытка найти связанный Obzor_partner объект для текущего партнёра
            obzor_id = ''
            if not partner.website:
                obzor = Obzor_partner.objects.filter(to_partner=partner).first()
                if obzor:
                    obzor_id = obzor.id

            # Подготовка данных для вывода партнёра
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

        # Добавляем отфильтрованных и отсортированных партнёров в категорию
        partners_prepared.append({
            'category': category,
            'partners': category_partners,
        })
    for i in partners_prepared:
        for i1 in i.items():
            print(i1)
    return render(request, "affiliate_program.html", context={"partners": partners_prepared,
                                                              'reklama': Reklama.objects.all().get(
                                                                  pos_reklama="1") if Reklama.objects.all().filter(
                                                                  pos_reklama="1").exists() else False,
                                                              "popup": Reklama.objects.all().get(
                                                                  pos_reklama="4") if Reklama.objects.all().filter(
                                                                  pos_reklama="4").exists() else False
                                                              })


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

    return render(request, "services.html", context={"services": services_prepared,
                                                     'reklama': Reklama.objects.all().get(
                                                         pos_reklama="1") if Reklama.objects.all().filter(
                                                         pos_reklama="1").exists() else False,
                                                     "popup": Reklama.objects.all().get(
                                                         pos_reklama="4") if Reklama.objects.all().filter(
                                                         pos_reklama="4").exists() else False
                                                     })


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
    if Reklama.objects.filter(pos_reklama="2").exists():
        url = Reklama.objects.get(pos_reklama="2").url
        photo = Reklama.objects.get(pos_reklama="2").photo

    a = []

    for i in range(3):
        a.append(Article.objects.all().filter(pos=str(i + 1)).exists())
        print(i, Article.objects.all().filter(pos=str(i + 1)).exists())

    if sum(a) == 3:
        positions = {
            '1': Article.objects.all().get(pos="1"),
            '2': Article.objects.all().get(pos="2"),
            '3': Article.objects.all().get(pos="3")}
        print(positions["1"].id)
    else:
        positions = False

    articles = []
    for article in Article.objects.all().order_by('-published_date')[0:8]:
        articles.append({
            'id': article.id,
            "image": article.image.url,
            "title": article.title,
            "content": article.content,
            "published_date": article.published_date,
            "is_case": article.is_case,
            "rating": article.rating,
            "username": article.author.username,
            "avatar": article.author.photo.url if article.author.photo else "https://protraffic.com/wp-content/themes/ptf/images/user.svg",
        })
    services = []
    for i in Service.objects.all().filter(to_index=True)[0:3]:
        services.append({
            'id': i.id,
            'descr': i.descr,
            'photo': i.photo.url,
            'website': i.website if i.website else f"/obzor/{Obzor.objects.filter(to_service=i)[0].id}",
            'promo': i.promo,
            'costs': i.costs,
            'category': i.category,
            'ifwebsite': True if i.website else False,
        })

    return render(request,
                  template_name="index.html",
                  context={"image": photo, "url_image": url,
                           "success": request.user.is_authenticated,
                           'positions': positions,
                           'MEDIA_URL': settings.MEDIA_URL,
                           'last_articles': articles,
                           'services': services,
                           'reklama3': Reklama.objects.all().get(
                               pos_reklama="3") if Reklama.objects.all().filter(
                               pos_reklama="3").exists() else False,
                           "popup": Reklama.objects.all().get(
                               pos_reklama="4") if Reklama.objects.all().filter(
                               pos_reklama="4").exists() else False})


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
    if not request.user.can_create_articles:
        messages.error(request, 'У вас нет прав для создания статей.')
        return redirect('profile')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.pos = "none"
            article.preview_for_index = "none"
            print(article)
            print(article)
            if request.user.is_partner:
                article.is_published = True  # Устанавливаем статус как "не опубликовано"
                article.save()
            else:
                article.is_published = False  # Устанавливаем статус как "не опубликовано"
                article.save()
                messages.success(request, 'Ваша статья отправлена на модерацию.')
            return redirect('user_articles')
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form})


def enable_article_creation(request):
    user = request.user
    user.can_create_articles = True
    user.save()
    return redirect('user_articles')  # Перенаправление на профиль пользователя или другую страницу


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'create_article.html'
    success_url = '/articles'  # Замените на нужный URL


def article_list(request):
    articles = Article.objects.filter(is_published=True).filter(is_case=False)[0:8]  # Извлекаем все статьи
    return render(request, 'articles.html', {'articles': articles,
    'reklama': Reklama.objects.all().get(pos_reklama="1") if Reklama.objects.all().filter(pos_reklama="1").exists() else False,
                                             "popup": Reklama.objects.all().get(
                                                 pos_reklama="4") if Reklama.objects.all().filter(
                                                 pos_reklama="4").exists() else False
})


def user_article_list(request):
    # Получаем текущего пользователя
    user = request.user
    # Фильтруем статьи по автору
    articles = Article.objects.all()
    return render(request, 'user_articles.html', {'articles': articles})


class UserArticleListView(ListView):
    model = Article
    template_name = 'user_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user
        if user.is_authenticated:
            # Фильтруем статьи по идентификатору автора
            return Article.objects.filter(author=user)
        else:
            return Article.objects.none()  # Возвращаем пустой QuerySet для неаутентифицированных пользователей



def partner_article_list(request):
    # Получаем текущего пользователя
    user = request.user
    # Фильтруем статьи по автору
    articles = Article.objects.all()
    return render(request, 'partner_articles.html', {'articles': articles})


class PartnerArticleListView(ListView):
    model = Article
    template_name = 'partner_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user
        if user.is_authenticated:
            # Фильтруем статьи по идентификатору автора
            return Article.objects.filter(author=user)
        else:
            return Article.objects.none()  # Возвращаем пустой QuerySet для неаутентифицированных пользователей



def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Получаем количество статей автора
    author_articles_count = Article.objects.filter(author=article.author).count()

    return render(request, 'article_detail.html', {
        'article': article,
        'author_articles_count': author_articles_count,
        'reklama': Reklama.objects.all().get(pos_reklama="2") if Reklama.objects.all().filter(pos_reklama="2").exists() else False
    })


def obzor_detail(request, obzor_id):
    obzor = get_object_or_404(Obzor, id=obzor_id)
    return render(request, 'obzor.html', {'obzor': obzor})


def obzorp_detail(request, obzor_id):
    obzor = get_object_or_404(Obzor_partner, id=obzor_id)
    return render(request, 'obzor.html', {'obzor': obzor})


def afcases(request):
    return render(request, 'affiliatecasestudy.html',
                  context={"articles": Article.objects.all().filter(is_case=True)[0:8],
                           'reklama': Reklama.objects.all().get(pos_reklama="1") if Reklama.objects.all().filter(
                               pos_reklama="1").exists() else False,
                           "popup": Reklama.objects.all().get(
                               pos_reklama="4") if Reklama.objects.all().filter(
                               pos_reklama="4").exists() else False
                           })


def article_add(request):
    page = int(request.GET.get('page', 1))
    category = request.GET.get('category', 1)
    articles_per_page = 8
    start = (page - 1) * articles_per_page
    end = start + articles_per_page
    print(start, end)

    # Рассчитываем начало и конец выборки

    # Получаем сервисы для текущей страницы
    if category == "a":
        articles = Article.objects.all().filter(is_case=False)[start:end]
    else:
        articles = Article.objects.all().filter(is_case=True)[start:end]

    articles_data = []

    for article in articles:
        articles_data.append({
            "image": article.image.url,
            "title": article.title,
            "content": article.content,
            "published_date": article.published_date,
            "is_case": article.is_case,
            "rating": article.rating,
            "username": article.author.username,
            "avatar": article.author.photo.url if article.author.photo else "https://protraffic.com/wp-content/themes/ptf/images/user.svg",
        })

    return JsonResponse(articles_data, safe=False)



@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Проверяем, является ли пользователь автором статьи или суперпользователем
    if request.user != article.author and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет прав для редактирования этой статьи.")

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('user_articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})


@login_required
def unpublish_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Проверяем права пользователя
    if request.user != article.author and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет прав для снятия статьи с публикации.")

    # Снимаем статью с публикации: меняем is_published и is_draft
    article.is_published = False
    article.is_draft = True
    article.save()

    return redirect('user_articles')


@login_required
def publish_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Проверяем права пользователя
    if request.user != article.author and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет прав для публикации статьи.")

    article.is_draft = False
    article.save()

    return redirect('user_articles')

