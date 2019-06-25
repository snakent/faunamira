from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User
from pages.animal.models import AnimalPhoto, Animal

class AnimalPhotosMixin(ContextMixin):
    """
    Вывод фотографий животного
    """
    def get_context_data(self, **kwargs):
        context = super(AnimalPhotosMixin, self).get_context_data(**kwargs)
        try:
            cur_animal = Animal.objects.filter(pk=self.kwargs.get('pk')).first()
        except:
            pass
        else:
            context['animal_photos'] = AnimalPhoto.objects.filter(animal=cur_animal)
        return context