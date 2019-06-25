from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.urls import reverse_lazy, reverse
from blocks.user import AuthFormMixin
from blocks.top_articles import TopArticlesMixin
from blocks.footer import FooterMixin
from django.contrib.auth.models import User
from pages.blog.models import Blog, BlogViewed
from pages.blog.forms import BlogForm
from django.core import serializers
import simplejson as json
from django.shortcuts import render
from blocks.banner import BannerMixin
from django.db.models import Q 
import datetime

def getBlogsView(request,blog_user=None):
    offset = int(request.POST.get('offset') or 0)
    search = request.POST.get('search')
    if blog_user:
        if search:
            articles = Blog.objects.filter(user__username=blog_user).filter( Q(article__contains=search) | Q(title__contains=search) )
        else:
            articles = Blog.objects.filter(user__username=blog_user)
        act_articles = Blog.get_actual_articles(articles=articles)
    else:
        if search:
            articles = Blog.objects.filter( Q(article__contains=search) | Q(title__contains=search) )
        else:
            articles = Blog.objects.all()
        act_articles = Blog.get_actual_articles(articles=articles)
    #return HttpResponse(json.dumps(serializers.serialize('json', act_articles[offset:offset+10])), content_type="application/json")
    return render(request, 'blog_list_ajax.html', {'blog_list':act_articles[offset:offset+3] })


class BlogListAllView(FooterMixin, BannerMixin, TopArticlesMixin, AuthFormMixin, ListView):
    """
    Все блоги
    """
    template_name = 'blog_list.html'
    context_object_name = 'blog_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search')
        return super(BlogListAllView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogListAllView, self).get_context_data(**kwargs)
        context['blog_list'] = self.get_queryset()[:3]
        context['settitle'] = 'Список блогов '
        return context

    def get_queryset(self):
        search = self.search
        if search:
            articles = Blog.objects.filter( Q(article__contains=search) | Q(title__contains=search) )
        else:
            articles = Blog.objects.all()
        act_articles = Blog.get_actual_articles(articles=articles)
        return act_articles


class BlogListView(FooterMixin, BannerMixin, TopArticlesMixin, AuthFormMixin, ListView):
    """
    Блог пользователя
    """
    template_name = 'blog_list.html'
    context_object_name = 'blog_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search')
        people = get_object_or_404(User, username=kwargs.get('username'))
        if people.is_active:
            return super(BlogListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        people = get_object_or_404(User, username=self.kwargs.get('username'))
        context['people'] = people
        context['blog_list'] = self.get_queryset()[:3]
        context['settitle'] = 'Список блогов пользователя ' + people.username
        return context

    def get_queryset(self):
        people = get_object_or_404(User, username=self.kwargs.get('username'))
        search = self.search
        if search:
            articles = Blog.objects.filter(user=people).filter( Q(article__contains=search) | Q(title__contains=search) )
        else:
            articles = Blog.objects.filter(user=people)
        act_articles = Blog.get_actual_articles(articles=articles)
        return act_articles


class BlogDetailView(FooterMixin, BannerMixin, TemplateView, AuthFormMixin):
    """
    Статья
    """
    model = Blog
    template_name = 'blog_detail.html'

    def get_people(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
        
    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs.get('pk'))
        author = blog.user
        #views
        user = request.user
        if user.is_authenticated and not self.kwargs.get('username'):
            people = get_object_or_404(User, username=user)
        #else:
        #    people = self.get_people()
        if user.is_authenticated and people != author:
            b_view = BlogViewed.objects.filter(blog_page=blog, user=user)
            if not b_view:
                blog.viewed += 1
                blog.save()
                b_vi = BlogViewed(blog_page=blog, user=user)
                b_vi.save()
        #
        if author.is_active:
            return super(BlogDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        this_object = get_object_or_404(Blog, pk=kwargs.get('pk'))
        context['object'] = this_object
        context['blog_animals'] = this_object.animals.all()
        context['settitle'] = 'Запись в блоге ' + this_object.title

        return context



class BlogCreateView(FooterMixin,CreateView):
    """
    Создание статьи
    """
    template_name = 'blog_create.html'
    model = Blog
    form_class = BlogForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_active:
            self.form_class = BlogForm
            self.form_class.user = user
            return super(BlogCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.date = datetime.datetime.now()
        obj.save()
        print(obj)
        return super(BlogCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.id})
    

"""
class BlogCreateView(FooterMixin,CreateView):

    template_name = 'blog_create.html'
    model = Blog
    form_class = BlogForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_active:
            self.form = BlogForm(user=user)
            return super(BlogCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(BlogCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.id})
"""

class BlogUpdateView(FooterMixin,UpdateView):
    """
    Редактирование статьи
    """
    template_name = 'blog_update.html'
    model = Blog
    form_class = BlogForm

    def get(self, request, *args, **kwargs):
        user = request.user
        self.obj = get_object_or_404(Blog, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            self.form_class = BlogForm
            self.form_class.instance = self.obj
            self.form_class.user = user
            return super(BlogUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(BlogUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.id})

"""
class BlogUpdateView(FooterMixin,UpdateView):

    template_name = 'blog_update.html'
    model = Blog
    form_class = BlogForm

    def get(self, request, *args, **kwargs):
        user = request.user
        self.obj = get_object_or_404(Blog, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            self.form = BlogForm(user=user,instance=self.obj)
            return super(BlogUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.id})
"""


class BlogDeleteView(FooterMixin,DeleteView):
    """
    Удаление статьи
    """
    template_name = 'blog_delete.html'
    model = Blog

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Blog, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            return super(BlogDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(BlogDeleteView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        return context

    def get_success_url(self):
        return reverse_lazy('blog_list', kwargs={'username': self.request.user})

