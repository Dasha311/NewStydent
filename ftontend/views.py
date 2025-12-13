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
    "kazwomensped": "university_generic.html",
    "krmu": "university_generic.html",
    "ksitch": "university_generic.html",
    "altu": "university_generic.html",
    "quniversity": "university_generic.html",
    "aga": "university_generic.html",
    "ageu": "university_generic.html",
    "aues": "university_generic.html",
    "educorp": "university_generic.html",
    "uib": "university_generic.html",
    "turan": "university_generic.html",
    "narxoz": "university_generic.html",
    "metu": "university_generic.html",
    "iit": "university_generic.html",
    "kazatiso": "university_generic.html",
    "cau": "university_generic.html",
    "symbat": "university_generic.html",
    "aes": "university_generic.html",
    "htu": "university_generic.html",
    "eim": "university_generic.html",
    "adi": "university_generic.html",
    "continuum": "university_generic.html",    
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
    {
        "slug": "kazwomensped",
        "title": "Казахский национальный женский педагогический университет",
        "description": "Профильный педагогический вуз с акцентом на подготовку учителей, психологов и специалистов инклюзивного образования.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/9/92/Kazakh_National_Women%27s_Teacher_Training_University.jpg",
        "city": "Алматы",
        "highlights": [
            "Методики преподавания и образовательная психология",
            "Центры практик в школах и детских садах",
            "Программы магистратуры и PhD по педагогике",
        ],
    },
    {
        "slug": "krmu",
        "title": "Казахстанско-Российский медицинский университет",
        "description": "Медицинский университет с клинической базой, симуляционными лабораториями и программами академической мобильности.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Kazakh-Russian_Medical_University_building.jpg",
        "city": "Алматы",
        "highlights": [
            "Лечебное дело, стоматология и фармация",
            "Практика в клиниках-партнёрах",
            "Международные стажировки и двойные дипломы",
        ],
    },
    {
        "slug": "ksitch",
        "title": "Казахстанско-Швейцарский институт туризма и гостиничного бизнеса",
        "description": "Институт, ориентированный на сервис, туризм и гостиничный менеджмент с международными стандартами обучения.",
        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Менеджмент в туризме и отельный бизнес",
            "Практико-ориентированное обучение",
            "Стажировки в индустрии гостеприимства",
        ],
    },
    {
        "slug": "altu",
        "title": "ALT University им. Мухамеджана Тынышпаева",
        "description": "Университет транспорта и логистики с инженерными и цифровыми программами для инфраструктурных отраслей.",
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Транспортная инженерия и логистика",
            "Цифровизация транспорта и управление инфраструктурой",
            "Партнёрства с отраслевыми компаниями",
        ],
    },
    {
        "slug": "quniversity",
        "title": "Q University",
        "description": "Университет с проектным обучением, предпринимательскими треками и упором на современные цифровые навыки.",
        "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Business & IT программы",
            "Инкубаторы и акселераторы для студентов",
            "Международные треки и обмен",
        ],
    },
    {
        "slug": "aga",
        "title": "Академия гражданской авиации (АГА)",
        "description": "Профильный вуз для подготовки пилотов, диспетчеров и инженеров авиационной отрасли.",
        "image": "https://images.unsplash.com/photo-1504204267155-aaad8e81290f?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Лётная подготовка и управление воздушным движением",
            "Инженерное обеспечение и техническое обслуживание",
            "Программы безопасности полётов",
        ],
    },
    {
        "slug": "ageu",
        "title": "Алматинский гуманитарно-экономический университет (АГЭУ)",
        "description": "Университет с экономическими, юридическими и гуманитарными программами для развития управленческих навыков.",
        "image": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Экономика, менеджмент и право",
            "Гуманитарные дисциплины",
            "Стажировки на предприятиях города",
        ],
    },
    {
        "slug": "aues",
        "title": "Алматинский университет энергетики и связи им. Г. Даукeева",
        "description": "Технический вуз в области энергетики, IT и телекоммуникаций с современными лабораториями и исследовательскими центрами.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6d/AUES_main_building.jpg",
        "city": "Алматы",
        "highlights": [
            "Электроэнергетика и теплоэнергетика",
            "Информационные технологии и телеком",
            "Инженерные программы с практикой",
        ],
    },
    {
        "slug": "educorp",
        "title": "Международная образовательная корпорация",
        "description": "Объединение профильных учебных заведений с архитектурными, дизайнерскими и строительными направлениями.",
        "image": "https://images.unsplash.com/photo-1503389152951-9f343605f61e?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Архитектура и дизайн среды",
            "Строительство и урбанистика",
            "Международные партнёрства в отрасли",
        ],
    },
    {
        "slug": "uib",
        "title": "Университет международного бизнеса (UIB)",
        "description": "Бизнес-университет с программами менеджмента, маркетинга, финансов и цифровой экономики.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/56/UIB_Almaty_campus.jpg",
        "city": "Алматы",
        "highlights": [
            "Бакалавриат и MBA по бизнес-направлениям",
            "Практические кейсы и стажировки",
            "Международные аккредитации",
        ],
    },
    {
        "slug": "turan",
        "title": "Университет «Туран»",
        "description": "Мультидисциплинарный университет с бизнес-, IT- и гуманитарными программами, творческими направлениями и развитой студенческой жизнью.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Turan_University_building.jpg",
        "city": "Алматы",
        "highlights": [
            "IT, бизнес и медиа",
            "Творческие индустрии",
            "Сильное студенческое сообщество",
        ],
    },
    {
        "slug": "narxoz",
        "title": "Нархоз университет",
        "description": "Экономический университет с современными программами в области финансов, аналитики данных и государственного управления.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Narxoz_University_main_building.jpg",
        "city": "Алматы",
        "highlights": [
            "Финансы, экономика и государственное управление",
            "Data analytics и цифровые навыки",
            "Карьерные сервисы и практика",
        ],
    },
    {
        "slug": "metu",
        "title": "Международный инженерно-технологический университет (METU)",
        "description": "Инженерно-технологический вуз с прикладными программами и акцентом на международное сотрудничество.",
        "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Инженерия и прикладные науки",
            "Технологический менеджмент",
            "Двойные дипломы и обмены",
        ],
    },
    {
        "slug": "iit",
        "title": "Международный университет информационных технологий (МУИТ)",
        "description": "IT-университет с программами по программной инженерии, кибербезопасности и медиа-технологиям.",
        "image": "https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Software Engineering и Cybersecurity",
            "MediaTech и game development",
            "Проектное обучение и хакатоны",
        ],
    },
    {
        "slug": "kazatiso",
        "title": "Казахская академия труда и социальных отношений (КазАТиСО)",
        "description": "Профильная академия по праву, социологии и управлению персоналом с практическими кейсами трудовых отношений.",
        "image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Юриспруденция и социально-трудовые отношения",
            "HR-менеджмент",
            "Повышение квалификации специалистов",
        ],
    },
    {
        "slug": "cau",
        "title": "Центрально-азиатский университет (Central Asian University)",
        "description": "Частный университет с современными программами менеджмента, IT и медицины, развивающий практические навыки студентов.",
        "image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Экономика, IT и здравоохранение",
            "Практика в собственных клиниках и лабораториях",
            "Гибкие учебные треки",
        ],
    },
    {
        "slug": "symbat",
        "title": "Академия дизайна и технологии «Сымбат»",
        "description": "Академия моды и дизайна с программами по fashion, текстилю и креативным индустриям.",
        "image": "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Fashion design и текстиль",
            "Дизайн костюма и аксессуаров",
            "Коллаборации с индустрией моды",
        ],
    },
    {
        "slug": "aes",
        "title": "Академия экономики и статистики",
        "description": "Специализированный вуз по экономике, статистике и аналитике данных для бизнеса и госуправления.",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Экономика и финансы",
            "Статистика и аналитика",
            "Прикладные кейсы и практика",
        ],
    },
    {
        "slug": "htu",
        "title": "Гуманитарно-технический университет",
        "description": "Университет, сочетающий технические и гуманитарные программы с практико-ориентированным подходом.",
        "image": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Инженерные и IT-направления",
            "Гуманитарные и социальные науки",
            "Проектные лаборатории",
        ],
    },
    {
        "slug": "eim",
        "title": "Евразийский институт рынка",
        "description": "Институт, специализирующийся на маркетинге, менеджменте и рыночной аналитике с фокусом на реальную практику.",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Маркетинг и PR",
            "Менеджмент и предпринимательство",
            "Аналитика рынка и потребителей",
        ],
    },
    {
        "slug": "adi",
        "title": "Автомобильно-дорожный институт",
        "description": "Институт транспортного строительства и сервиса с практикой в дорожной отрасли и автомобильной инженерии.",
        "image": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Строительство и эксплуатация дорог",
            "Автомобильный транспорт и сервис",
            "Лаборатории дорожных материалов",
        ],
    },
    {
        "slug": "continuum",
        "title": "Университет непрерывного образования",
        "description": "Университет для взрослых и профессионалов с гибкими программами повышения квалификации и переподготовки.",
        "image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80",
        "city": "Алматы",
        "highlights": [
            "Гибкие форматы обучения",
            "Программы для карьерного роста",
            "Онлайн и офлайн треки",
        ],
    },
    
]

BRAND_STYLES = {
    "almau": {"brand_color": "#D62828", "brand_color_soft": "rgba(214, 40, 40, 0.12)"},
    "satbayev": {"brand_color": "#0F766E", "brand_color_soft": "rgba(15, 118, 110, 0.12)"},
    "kbtu": {"brand_color": "#1D4ED8", "brand_color_soft": "rgba(29, 78, 216, 0.12)"},
    "nu": {"brand_color": "#111827", "brand_color_soft": "rgba(17, 24, 39, 0.12)"},
    "kaznu": {"brand_color": "#0EA5E9", "brand_color_soft": "rgba(14, 165, 233, 0.12)"},
    "kaznmu": {"brand_color": "#16A34A", "brand_color_soft": "rgba(22, 163, 74, 0.12)"},
    "kaznpu": {"brand_color": "#D97706", "brand_color_soft": "rgba(217, 119, 6, 0.12)"},
    "kazumo": {"brand_color": "#DB2777", "brand_color_soft": "rgba(219, 39, 119, 0.12)"},
    "technological": {"brand_color": "#7C3AED", "brand_color_soft": "rgba(124, 58, 237, 0.12)"},
    "german": {"brand_color": "#2563EB", "brand_color_soft": "rgba(37, 99, 235, 0.12)"},
    "sports": {"brand_color": "#F97316", "brand_color_soft": "rgba(249, 115, 22, 0.12)"},
    "arts": {"brand_color": "#A855F7", "brand_color_soft": "rgba(168, 85, 247, 0.12)"},
    "auezov": {"brand_color": "#059669", "brand_color_soft": "rgba(5, 150, 105, 0.12)"},
    "buketov": {"brand_color": "#B45309", "brand_color_soft": "rgba(180, 83, 9, 0.12)"},
    "narxoz": {"brand_color": "#BE123C", "brand_color_soft": "rgba(190, 18, 60, 0.12)"},
    "turan": {"brand_color": "#0EA5E9", "brand_color_soft": "rgba(14, 165, 233, 0.12)"},
}

for university in UNIVERSITY_LIST:
    styles = BRAND_STYLES.get(university["slug"])
    if styles:
        university.update(styles)


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

