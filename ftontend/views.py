from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from .forms import LoginForm, RegistrationForm

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
    "almau": "university_almau.html",
    "nu": "university_nu.html",
    "kbtu": "university_kbtu.html",
    "auezov": "university_auezov.html",
    "buketov": "university_buketov.html",    
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
    "10": "almau",
    "11": "nu",
    "12": "kbtu",    
}

UNIVERSITY_LIST = [
    {
        "slug": "kaznu",
        "title": "КазНУ им. аль-Фараби",
        "description": "Ведущий классический университет Казахстана с сильными научными школами и международными программами.",
        "image": "https://tse4.mm.bing.net/th/id/OIP.04VoTSK8TSPRiA37Jf06sAHaEK?rs=1&pid=ImgDetMain&o=7&rm=3",
        "city": "Алматы",
    },
    {
        "slug": "kaznpu",
        "title": "КазНПУ им. Абая",
        "description": "Главный педагогический университет страны с богатой историей подготовки учителей и методистов.",
        "image": "https://th.bing.com/th/id/R.a80632595b0d22985d2cbf690c2b5e6b?rik=6De7vETNPPDf1A&pid=ImgRaw&r=0",
        "city": "Алматы",        
    },
    {
        "slug": "kaznmu",
        "title": "КазНМУ им. С.Д. Асфендиярова",
        "description": "Крупнейший медицинский вуз Казахстана с современной клинической базой и симуляционными центрами.",
        "image": "https://cdn.nur.kz/images/1120x630/3e1dc070e20b67a0.jpeg",
        "city": "Алматы",
    },
    {
        "slug": "satbayev",
        "title": "Satbayev University",
        "description": "Инженерно-технический лидер региона с акцентом на цифровые технологии и партнерство с индустрией.",
        "image": "https://tse3.mm.bing.net/th/id/OIP.fHBO3n4VzN_s2JN-kPfOoAHaFj?rs=1&pid=ImgDetMain&o=7&rm=3",
        "city": "Алматы",
    },
    {
        "slug": "kazumo",
        "title": "КазУМОиМЯ им. Абылай хана",
        "description": "Специализируется на международных отношениях, переводе и глобальной коммуникации.",
        "image": "https://th.bing.com/th/id/R.a7e1d3b6835fc0480ad4c4c0128f2c06?rik=PbgHjtH%2bEMmdSw&pid=ImgRaw&r=0",
        "city": "Алматы",
    },
    {
        "slug": "technological",
        "title": "Алматинский технологический университет",
        "description": "Лидер в сфере пищевых технологий, дизайна и лёгкой промышленности.",
        "image": "https://th.bing.com/th/id/R.48b3ae67ed7c4a0649ae58f7b0df23df?rik=XiI6BEVUzIDWwg&pid=ImgRaw&r=0",
        "city": "Алматы",
    },
    {
        "slug": "german",
        "title": "Казахстанско-Немецкий университет",
        "description": "Мост между Казахстаном и Европой с программами на немецком и английском языках.",
        "image": "https://tse1.mm.bing.net/th/id/OIP.VhJ_8aDNg_1JjkuOzyh87AHaEK?rs=1&pid=ImgDetMain&o=7&rm=3",
        "city": "Алматы",
    },
    {
        "slug": "sports",
        "title": "Казахская академия спорта и туризма",
        "description": "Подготовка спортсменов, тренеров и специалистов индустрии спорта мирового уровня.",
        "image": "https://tse2.mm.bing.net/th/id/OIP.2Xt9ipdlx0nZ7VqdM7_4_QHaE6?rs=1&pid=ImgDetMain&o=7&rm=3",
        "city": "Алматы",
    },
    {
        "slug": "arts",
        "title": "Казахская национальная академия искусств им. Т. К. Жургенова",
        "description": "Центр художественного образования: театр, кино, музыка, дизайн и анимация.",
        "image": "https://th.bing.com/th/id/R.387367e7f691cdc69b7fd58b693d1941?rik=y8fdWXONddr6qw&pid=ImgRaw&r=0",
        "city": "Алматы",
    },
    {
        "slug": "almau",
        "title": "Almaty Management University",
        "description": "Предпринимательский университет, где соединяются бизнес-образование, технологические навыки и ESG-повестка.",
        "image": "https://tse2.mm.bing.net/th/id/OIP.jmnQ2nXpWCuNWgmBDhCSbwHaEL?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3",
        "city": "Алматы",
    },
    {
        "slug": "nu",
        "title": "Назарбаев Университет",
        "description": "Исследовательский университет в Астане, работающий по международным стандартам и развивающий STEM-навыки.",
        "image": "https://smapse.com/storage/2019/09/x1-3.jpg",
        "city": "Астана",
    },
    {
        "slug": "kbtu",
        "title": "Казахстанско-Британский Технический Университет",
        "description": "Ведущий технический вуз Казахстана с сильными программами в области IT, инженерии и энергетики.",
        "image": "https://th.bing.com/th/id/R.8a9e84a375233bde57ac81c71c7ea967?rik=2DxCpttiUCRyQw&pid=ImgRaw&r=0",
        "city": "Алматы",
    },
    {
        "slug": "auezov",
        "title": "Южно-Казахстанский университет им. М. Ауэзова",
        "description": "Крупнейший университет юга Казахстана с сильными инженерными, аграрными и гуманитарными программами.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/2a/M.Auezov_South_Kazakhstan_University.jpg",
        "city": "Шымкент",        
    },
    {
        "slug": "buketov",
        "title": "Карагандинский университет им. Е. А. Букетова",
        "description": "Классический университет Центрального Казахстана с акцентом на фундаментальные науки и педагогическое образование.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Karaganda_State_University.jpg/1200px-Karaganda_State_University.jpg",
        "city": "Караганда",
    },

    
]

UNIVERSITY_DATA = {university["slug"]: university for university in UNIVERSITY_LIST}

def main_menu(request):
    return render(request, "MainMenu.html")


def about(request):
    return render(request, "about.html")


def contacts(request):
    return render(request, "contact.html")


def auth_view(request):
    show_register = request.GET.get("mode") == "register"
    login_form = LoginForm(request=request)
    register_form = RegistrationForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "login":
            login_form = LoginForm(request.POST, request=request)
            register_form = RegistrationForm()
            if login_form.is_valid():
                login(request, login_form.get_user())
                messages.success(request, "Вы успешно вошли в систему.")
                return redirect("main_menu")
        elif form_type == "register":
            register_form = RegistrationForm(request.POST)
            login_form = LoginForm(request=request)
            show_register = True
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect("main_menu")

    context = {
        "login_form": login_form,
        "register_form": register_form,
        "show_register": show_register,
    }
    return render(request, "auth.html", context)


def course_view(request):
    course_id = request.GET.get("course_id")
    if course_id:
        slug = COURSE_ID_TO_SLUG.get(course_id)
        if not slug:
            raise Http404("Университет не найден")
        return redirect("university_detail", slug=slug)

    selected_city = request.GET.get("city", "all")
    if selected_city != "all":
        filtered_universities = [
            university
            for university in UNIVERSITY_LIST
            if university["city"] == selected_city
        ]
    else:
        filtered_universities = UNIVERSITY_LIST

    paginator = Paginator(filtered_universities, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    cities = sorted({university["city"] for university in UNIVERSITY_LIST})

    context = {
        "page_obj": page_obj,
        "cities": cities,
        "selected_city": selected_city,
    }
    return render(request, "university_list.html", context)


def university_detail(request, slug: str):
    template_name = UNIVERSITY_TEMPLATES.get(slug)
    if not template_name:
        raise Http404("Университет не найден")
    university = UNIVERSITY_DATA.get(slug)
    if not university:
        raise Http404("Университет не найден")

    context = {"university": university}
    return render(request, template_name, context)


def video_detail(request):
    return render(request, "video_detail.html")


def video_detail2(request):
    return render(request, "video_detail2.html")


def video_detail3(request):
    return render(request, "video_detail3.html")

