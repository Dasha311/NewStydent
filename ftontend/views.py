from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import Http404
from django.shortcuts import redirect, render

UNIVERSITY_TEMPLATES = {
    "kaznu": "university_kaznu.html",
    "kaznpu": "university_kaznpu.html",
    "kaznmu": "university_kaznmu.html",
    "satbayev": "university_satbayev.html",
    "kazumo": "university_kazumo.html",
    "technological": "university_technological.html",
    "german": "university_german.html",
    "sports": "university_sports.html",
    "arts": "university_arts.html",
}

COURSE_ID_TO_SLUG = {
    "1": "kaznu",
    "2": "kaznpu",
    "3": "kaznmu",
    "4": "satbayev",
    "5": "kazumo",
    "6": "technological",
    "7": "german",
    "8": "sports",
    "9": "arts",
}

UNIVERSITY_LIST = [
    {
        "slug": "kaznu",
        "title": "КазНУ им. аль-Фараби",
        "description": "Ведущий классический университет Казахстана с сильными научными школами и международными программами.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Al-Farabi_Kazakh_National_University_main_building.jpg",
    },
    {
        "slug": "kaznpu",
        "title": "КазНПУ им. Абая",
        "description": "Главный педагогический университет страны с богатой историей подготовки учителей и методистов.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/56/Akhmet_Baitursynuly_Street_13_Almaty_02.jpg",
    },
    {
        "slug": "kaznmu",
        "title": "КазНМУ им. С.Д. Асфендиярова",
        "description": "Крупнейший медицинский вуз Казахстана с современной клинической базой и симуляционными центрами.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/4f/S.D._Asfendiyarov_Kazakh_National_Medical_University.jpg",
    },
    {
        "slug": "satbayev",
        "title": "Satbayev University",
        "description": "Инженерно-технический лидер региона с акцентом на цифровые технологии и партнерство с индустрией.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Kazakh-British_Technical_University.jpg",
    },
    {
        "slug": "kazumo",
        "title": "КазУМОиМЯ им. Абылай хана",
        "description": "Специализируется на международных отношениях, переводе и глобальной коммуникации.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/27/Ablai_Khan_University.jpg",
    },
    {
        "slug": "technological",
        "title": "Алматинский технологический университет",
        "description": "Лидер в сфере пищевых технологий, дизайна и лёгкой промышленности.",
        "image": "https://tengrinews.kz/userdata/news/2017/news_326837/thumb_m/photo_219423.png",
    },
    {
        "slug": "german",
        "title": "Казахстанско-Немецкий университет",
        "description": "Мост между Казахстаном и Европой с программами на немецком и английском языках.",
        "image": "https://dku.kz/assets/files/000/000/378/original/DSC_3159.jpg",
    },
    {
        "slug": "sports",
        "title": "Казахская академия спорта и туризма",
        "description": "Подготовка спортсменов, тренеров и специалистов индустрии спорта мирового уровня.",
        "image": "https://almaty.tv/storage/news/2018/07/26/1532588549196122.jpeg",
    },
    {
        "slug": "arts",
        "title": "Казахская национальная академия искусств им. Т. К. Жургенова",
        "description": "Центр художественного образования: театр, кино, музыка, дизайн и анимация.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Kazakh_National_Academy_of_Arts.jpg",
    },
]


def main_menu(request):
    return render(request, "MainMenu.html")


def about(request):
    return render(request, "about.html")


def contacts(request):
    return render(request, "contact.html")


def course_view(request):
    course_id = request.GET.get("course_id")
    if course_id:
        slug = COURSE_ID_TO_SLUG.get(course_id)
        if not slug:
            raise Http404("Университет не найден")
        return redirect("university_detail", slug=slug)

    context = {"universities": UNIVERSITY_LIST}
    return render(request, "university_list.html", context)


def university_detail(request, slug: str):
    template_name = UNIVERSITY_TEMPLATES.get(slug)
    if not template_name:
        raise Http404("Университет не найден")
    return render(request, template_name)


def video_detail(request):
    return render(request, "video_detail.html")


def video_detail2(request):
    return render(request, "video_detail2.html")


def video_detail3(request):
    return render(request, "video_detail3.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("profile")
    else:
        form = AuthenticationForm(request)

    return render(request, "auth/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("profile")
    else:
        form = UserCreationForm()

    return render(request, "auth/register.html", {"form": form})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "profile.html")


def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect("main_menu")


def delete_account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        user = request.user
        auth_logout(request)
        user.delete()
        return redirect("main_menu")

    return render(request, "account/delete_account.html")