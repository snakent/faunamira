from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BlogConfig(AppConfig):
    name = 'pages.blog'
    verbose_name = _('Blog')
    verbose_name_plural = _('Blog records')
