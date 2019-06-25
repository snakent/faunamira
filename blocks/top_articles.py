from django.views.generic.base import ContextMixin
from pages.blog.models import Blog


class TopArticlesMixin(ContextMixin):
    """
    Последние записи в блоге
    """
    def get_context_data(self, **kwargs):
        context = super(TopArticlesMixin, self).get_context_data(**kwargs)
        # articles = Blog.objects.filter(user__is_active=True).order_by('-date')[:4]
        articles = Blog.objects.all().order_by('-viewed')[:10]
        context['top_articles'] = articles
        return context