from django.views.generic.base import ContextMixin
from refdata.models import City


class CitiesMixin(ContextMixin):
    """
    Список городов
    """
    def get_context_data(self, **kwargs):
        context = super(CitiesMixin, self).get_context_data(**kwargs)
        cities_list = City.objects.filter(country_id__code='RU').order_by('name_ru').values('name_ru','pk').distinct()
        context['cities_list'] = cities_list
        return context