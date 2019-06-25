from django.db import models
from dry_library.backend.thumbnails import CreateThumbnail
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from tinymce import models as tinymce_model


class Banner(models.Model):
    """
    Модель для баннера
    """
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Banner name'))
    # content = tinymce_model.HTMLField(blank=True, verbose_name=_('Banner content'))
    image = models.ImageField(max_length=100, upload_to='banner', blank=True, null=True,
                               verbose_name=_('Banner'))
    status = models.BooleanField(default=False, verbose_name=_('Active status'))

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return self.title


class AltMenu(models.Model):
    """
    Модель для альтернативного меню
    """
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    url = models.URLField(max_length=50, blank=False, verbose_name=_('Url'))
    order = models.PositiveIntegerField(blank=False, verbose_name=_('order'))
    slug = models.SlugField(max_length=30, blank=True, null=True, verbose_name=_('Slug'))

    class Meta:
        verbose_name = _('Additional menu')
        verbose_name_plural = _('Additional menu')
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Создание slug из title
        """
        self.slug = slugify(self.title)
        super(AltMenu, self).save(*args, **kwargs)


class SocialLink(models.Model):
    """
    Ссылки на социальные сети
    """
    TYPES = (                           # Варианты социальных сетей
        ('vk', _('Vkontakte')),
        ('ok', _('Odnoklassniki')),
        ('fb', _('Facebook')),
        ('in', _('Instagram')),
    )
    title = models.CharField(max_length=2, choices=TYPES, blank=False, verbose_name=_('Title'))
    url = models.URLField(max_length=50, blank=False, verbose_name=_('Url'))

    class Meta:
        verbose_name = _('Social links')
        verbose_name_plural = _('Social links')

    def __str__(self):
        return self.title


class Country(models.Model):
    """
    Справочник стран
    """    
    name_ru = models.CharField(max_length=100, verbose_name=_('Name ru'))
    name_en = models.CharField(max_length=100, verbose_name=_('Name en'))
    code = models.CharField(max_length=2, verbose_name=_('Code'))

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countrys')

    def __str__(self):
        return self.name_ru


class City(models.Model):
    """
    Справочник городов
    """
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Country'))
    name_ru = models.CharField(max_length=100, verbose_name=_('Name ru'))
    name_en = models.CharField(max_length=100, verbose_name=_('Name en'))
    region = models.CharField(max_length=2, verbose_name=_('Region'))
    postal_code = models.CharField(max_length=10, verbose_name=_('Postal code'))
    latitude = models.FloatField(max_length=10.6, null=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(max_length=10.6, null=True, verbose_name=_('Longitude'))
    population = models.IntegerField(null=True, default=0, verbose_name=_('Population'))
    ontop = models.IntegerField(null=True, default=0, verbose_name=_('On top'))

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name_ru



class FilterLogo(CreateThumbnail, models.Model):
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Название'))
    srcimage = models.ImageField(max_length=100, upload_to='logo', blank=True, null=True,
                               verbose_name=_('Исходное изображение'))
    image = models.ImageField(max_length=100, upload_to='logo/thumbnail', blank=True, null=True,
                               verbose_name=_('Изображение'))
    status = models.BooleanField(default=False, verbose_name=_('Активность'))

    class Meta:
        verbose_name = _('Логотип фильтра')
        verbose_name_plural = _('Логотипы фильтра')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        try:
            this_record = FilterLogo.objects.get(pk=self.pk)
            if this_record.srcimage != self.srcimage:
                this_record.srcimage.delete(save=False)
                this_record.image.delete(save=False)
        except:
            pass

        self.create_thumbnail(width=910, height=410, from_img=self.srcimage, to_img=self.image)
        super(FilterLogo, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.srcimage.delete(save=False)
        self.image.delete(save=False)
        super(FilterLogo, self).delete(*args, **kwargs)