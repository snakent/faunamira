from django.views.generic.base import ContextMixin
from refdata.models import FilterLogo
from random import randint

class FilterLogoMixin(ContextMixin):
    """
    Примись логотипа
    """
    def get_context_data(self, **kwargs):
        context = super(FilterLogoMixin, self).get_context_data(**kwargs)
        active_banners = FilterLogo.objects.filter(status=True)
        if active_banners:
            count = len(active_banners)
            random_index = randint(0, count-1)
            context['filterlogo'] = active_banners[random_index].image
        return context