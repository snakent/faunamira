from django.views.generic import TemplateView
from django.utils.timezone import now
from django.template import loader
from django.http import JsonResponse
from datetime import date

from pages.animal.models import Animal, AnimalAttr
from pages.userprofile.models import Profile, ProfileAbout

from blocks.user import AuthFormMixin
from blocks.my_animals import MyAnimalsMixin
from blocks.panel_filters import FiltersMixin
from blocks.banner import BannerMixin
from blocks.random_profiles import RandomProfilesMixin
from blocks.top_profiles import TopProfilesMixin
from blocks.latest_articles import LatestArticlesMixin
from blocks.footer import FooterMixin
from blocks.cities import CitiesMixin
from blocks.filterlogo import FilterLogoMixin
from django.db.models import Q

class HomeView(CitiesMixin, BannerMixin, FilterLogoMixin,FiltersMixin, RandomProfilesMixin, TopProfilesMixin, MyAnimalsMixin, LatestArticlesMixin,
               FooterMixin, AuthFormMixin, TemplateView):
    template_name = 'home.html'

def get_animal_results(request):
    """
    Получение результатов поиска по животным
    """
    if request.is_ajax:
        kind = request.POST.get('kind')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        age = request.POST.get('age')
        agelist=age.split('-')
        status = request.POST.get('status')
        breed = request.POST.get('breed')
        offset = int(request.POST.get('offset') or 0)+12

        query = Animal.objects.all()
        compl = True                            # статус поиска

        if status:
            new_query = query.filter(status=status)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if kind:
            new_query = query.filter(kind__kind=kind)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if breed:
            breed_attr = AnimalAttr.objects.filter(attr__attr='Порода', kind__kind=kind, value__value=breed)
            new_query = query.filter(id__in=list(breed_attr.values_list('animal', flat=True)))
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if gender:
            new_query = query.filter(gender=gender)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if city:
            new_query = query.filter(user__profile__city__name_ru=city)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if age:
            if agelist[0]:
                agemin = int(agelist[0]) or 0
            else:
                agemin = 0
            if agelist[1]:
                agemax = int(agelist[1]) or 999
            else:
                agemax = 999
            cur_date = now().date()
            max_date = date(cur_date.year - agemin, cur_date.month, cur_date.day)
            min_date = date(cur_date.year - agemax - 1, cur_date.month, cur_date.day)
            if not agemin:
                max_date=cur_date
            new_query = query.filter(birthday__lte=max_date, birthday__gt=min_date)
            if not agemax:
                new_query = query.filter(birthday__lte=max_date)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False

        if query.count()==len(query[:offset]):
            search_moar=None
        else:
            search_moar=True

        context = {
            'animal_results': query[:offset],
            'compl': compl,
            'search_offset': offset,
            'search_type' : 'a',
            'search_moar' : search_moar,
            'settitle' : 'Поиск животных'
        }
        html_content = loader.render_to_string(template_name='include/results.html', context=context)

        data = {
            'html_content': html_content,
        }
        return JsonResponse(data)


def get_people_results(request):
    """
    Получение результатов поиска по людям
    """
    if request.is_ajax:
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        agelist=age.split('-')
        city = request.POST.get('city')
        purpose = request.POST.get('purpose')
        offset = int(request.POST.get('offset') or 0)+12

        query = Profile.objects.filter(user__is_active=True)
        compl = True

        if gender:
            new_query = query.filter(gender=gender)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if age:
            if agelist[0]:
                agemin = int(agelist[0]) or 0
            else:
                agemin = 0
            if agelist[1]:
                agemax = int(agelist[1]) or 999
            else:
                agemax = 999
            cur_date = now().date()
            max_date = date(cur_date.year - agemin, cur_date.month, cur_date.day)
            min_date = date(cur_date.year - agemax - 1, cur_date.month, cur_date.day)
            if not agemin:
                max_date=cur_date
            new_query = query.filter(birthday__lte=max_date, birthday__gt=min_date)
            if not agemax:
                new_query = query.filter(birthday__lte=max_date)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if purpose:
            new_query = query.filter(user__about__purpose=purpose)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if city:
            new_query = query.filter(city__name_ru=city)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False

        if query.count()==len(query[:offset]):
            search_moar=None
        else:
            search_moar=True

        context = {
            'compl': compl,
            'people_results': query[:offset],
            'search_offset': offset,
            'search_type' : 'p',
            'search_moar' : search_moar,
            'settitle' : 'Поиск людей'
        }

        html_content = loader.render_to_string(template_name='include/results.html', context=context)

        data = {
            'html_content': html_content,
        }
        return JsonResponse(data)