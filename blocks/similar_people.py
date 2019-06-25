from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User
from pages.userprofile.models import Profile

from dry_library.backend.similar_people import get_similar_people

class SimilarProfilesMixin(ContextMixin):
    """
    Вывод животных пользователя
    """
    def get_context_data(self, **kwargs):
        context = super(SimilarProfilesMixin, self).get_context_data(**kwargs)
        try:
            cur_user = self.kwargs.get('username')#self.request.user.username
            people = User.objects.get(username=cur_user)
            context['similar_people'] = get_similar_people(people,people)
        except:
            pass
        return context
