from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from pages.animal.models import Animal, AnimalAttr, KindAnimalAttr,KindAnimal,KindAnimalAttrVal,AnimalPhoto,AnimalViewed
from pages.blog.models import Blog

from pages.animal.forms import AnimalForm, AnimalAttrForm,AnimalUpdAttrForm,AnimalPhotoForm
from blocks.banner import BannerMixin
from django.http import JsonResponse
from django.shortcuts import render
import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from blocks.footer import FooterMixin
from blocks.user import AuthFormMixin
from blocks.my_animals import MyAnimalsMixin
from blocks.animal_photos import AnimalPhotosMixin

from dry_library.backend.similar_people import get_similar_animal


def getAnimalsView(request):
    dict_animals = {}
    kinds = KindAnimal.objects.all().order_by('kind')
    dict_kinds = {}
    for kind in kinds:
        attrs = KindAnimalAttr.objects.filter(kind=kind).order_by('attr')
        dict_attrs = {}
        for attr in attrs:
            values = KindAnimalAttrVal.objects.filter(attr=attr).order_by('value')
            list_values = values.values_list('value', flat=True)
            new = {}
            for e in values:
                new[e.pk]=str(e)
            dict_attrs[attr.attr]=new
        dict_kinds[kind.kind]=dict_attrs
    dict_animals = dict_kinds
    return HttpResponse(json.dumps(dict_animals), content_type="application/json")


class AnimalView(AnimalPhotosMixin, FooterMixin, BannerMixin, AuthFormMixin, TemplateView):
    """
    Страница профиля животного
    """
    template_name = 'animal.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        animal = get_object_or_404(Animal, id=kwargs.get('pk'))
        owner = animal.user
        if owner.is_active:
            prof_view = True
            if user.is_authenticated and not user==owner:
                prof_view = AnimalViewed.objects.filter(profile_page=user, animal=animal)
            if not prof_view:
                animal.viewed += 1
                animal.save()
                an_vi = AnimalViewed(profile_page=user, animal=animal)
                an_vi.save()
            return super(AnimalView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(AnimalView, self).get_context_data(**kwargs)
        people = get_object_or_404(Animal, pk=self.kwargs.get('pk')).user
        animal=get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        context['animal'] = animal
        context['attrs'] = AnimalAttr.objects.filter(animal__pk=self.kwargs.get('pk'))
        context['people'] = people
        context['stat_viewed'] = animal.viewed
        context['in_blog'] = Blog.objects.filter(animals__pk=animal.pk)
        context['similar_animals'] = get_similar_animal(animal)
        context['more_animals'] = Animal.objects.filter(user=people).exclude(pk=animal.pk)
        context['settitle'] = 'Страница животного ' + animal.first_name
        return context


class AnimalCreateView(MyAnimalsMixin,FooterMixin,AuthFormMixin,CreateView):
    """
    Создание профиля животного
    """
    template_name = 'animal_create.html'
    model = Animal
    form_class = AnimalForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return super(AnimalCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AnimalCreateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['settitle'] = 'Мои питомцы'
        return context

    def post(self, request, *args, **kwargs):
        animalform = self.form_class(request.POST)
        if animalform.is_valid():
            data = animalform.save(commit=False)
            data.user = self.request.user
            data.save()
            self.object = data
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(context={'form': animalform})


class AnimalUpdateView(FooterMixin,AuthFormMixin,UpdateView):
    """
    Редактирование животного
    """
    model = Animal
    template_name = 'animal_update.html'
    form_class = AnimalForm

    def get_animal(self):
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        return animal

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_animal()
        if (self.object.user == request.user) and self.object.user.is_active:
            self.form = AnimalForm(instance=self.object)
            return super(AnimalUpdateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AnimalUpdateView, self).get_context_data(**kwargs)
        animal = self.get_animal()
        context['form'] = self.form_class(instance=animal)
        context['animal'] = animal
        return context


class AnimalDeleteView(FooterMixin,AuthFormMixin,DeleteView):
    """
    Удаление животного
    """
    template_name = 'animal_delete.html'
    model = Animal

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Animal, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            return super(AnimalDeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AnimalDeleteView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        return context

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'username': self.request.user})


class AttrCreateView(FooterMixin,AuthFormMixin,CreateView):
    """
    Добавления харатеристик животному
    """
    template_name = 'attr_create.html'
    model = AnimalAttr
    form_class = AnimalAttrForm

    def get_animal(self):
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        return animal

    def get_form(self):
        form = super(AttrCreateView, self).get_form()
        form.fields['attr'].queryset = KindAnimalAttr.objects.filter(kind=self.get_animal().kind)
        return form

    def get(self, request, *args, **kwargs):
        animal = self.get_animal()
        if (request.user == animal.user) and animal.user.is_active:
            return super(AttrCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def form_valid(self, form):
        animal = self.get_animal()
        obj = form.save(commit=False)
        obj.animal = animal
        obj.kind = animal.kind
        return super(AttrCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        animal = self.get_animal()
        context = super(AttrCreateView, self).get_context_data(**kwargs)
        context['animal'] = self.get_animal()
        context['form'] = self.form_class(instance=animal)
        return context


    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.kwargs.get('pk')})


class AttrUpdateView(FooterMixin,AuthFormMixin,UpdateView):
    """
    Редактирование атрибута
    """
    model = AnimalAttr
    template_name = 'attr_update.html'
    form_class = AnimalUpdAttrForm

    def get_attr(self):
        return get_object_or_404(AnimalAttr, pk=self.kwargs.get('pk'))

    def get_form(self):
        form = super(AttrUpdateView, self).get_form()
        form.fields['attr'].queryset = KindAnimalAttr.objects.filter(kind=self.object.kind)
        return form

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.animal.pk})

    def get(self, request, *args, **kwargs):
        self.obj = self.get_attr()
        if (self.obj.animal.user == self.request.user) and self.obj.animal.user.is_active:
            self.form = AnimalUpdAttrForm(instance=self.obj)
            return super(AttrUpdateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        animal = get_object_or_404(Animal, pk=self.obj.animal.pk)
        context = super(AttrUpdateView, self).get_context_data(**kwargs)
        context['animal'] = animal
        context['form'] = self.form_class(instance=self.obj)
        return context


class AttrDeleteView(FooterMixin,AuthFormMixin,DeleteView):
    """
    Удаление атрибута
    """
    template_name = 'attr_delete.html'
    model = AnimalAttr

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(AnimalAttr, pk=self.kwargs["pk"])
        if (self.object.animal.user == request.user) and self.object.animal.user.is_active:
            return super(AttrDeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AttrDeleteView, self).get_context_data(**kwargs)
        context['animal'] = self.object.animal
        context['obj'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.animal.pk})


class PhotoCreateView(FooterMixin,AuthFormMixin,CreateView):
    """
    Добавление фото
    """
    template_name = 'photo_create.html'
    model = AnimalPhoto
    form_class = AnimalPhotoForm

    def get_animal(self):
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        return animal

    def get(self, request, *args, **kwargs):
        animal = self.get_animal()
        if (request.user == animal.user) and animal.user.is_active:
            return super(PhotoCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def form_valid(self, form):
        animal = self.get_animal()
        obj = form.save(commit=False)
        obj.animal = animal
        return super(PhotoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        animal = self.get_animal()
        context = super(PhotoCreateView, self).get_context_data(**kwargs)
        context['animal'] = animal
        context['form'] = self.form_class(instance=animal)
        return context

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.kwargs.get('pk')})


class PhotoDeleteView(FooterMixin,AuthFormMixin,DeleteView):
    """
    Удаление фото
    """
    template_name = 'photo_delete.html'
    model = AnimalPhoto

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(AnimalPhoto, pk=self.kwargs["pk"])
        if (self.object.animal.user == request.user) and self.object.animal.user.is_active:
            return super(PhotoDeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(PhotoDeleteView, self).get_context_data(**kwargs)
        context['animal'] = self.object.animal
        context['obj'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.animal.pk})
        