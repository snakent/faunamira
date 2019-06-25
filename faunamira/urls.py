"""faunamira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from faunamira import settings
from django.contrib.auth import views as auth_views
from blocks import user

urlpatterns = [
    # админка
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),

    # авторизация
    url(r'^accounts/', include('allauth.urls')),

    # редактор текста
    url(r'^tinymce/', include('tinymce.urls')),

    # страницы
    url(r'^', include('pages.home.urls')),
    url(r'^profile/', include('pages.userprofile.urls')),
    url(r'^animal/', include('pages.animal.urls')),
    url(r'^blog/', include('pages.blog.urls')),
    url(r'^dialogs/', include('pages.messager.urls')),

    # блоки
    url(r'^user_login/$', user.user_login, name='user_login'),
    url(r'^user_signup/$', user.user_signup, name='user_signup'),

    #chat
    url(r'^chat/', include('chat.urls')),

    #password reset
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
