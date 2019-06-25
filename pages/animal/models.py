from django.db import models
from dry_library.backend.thumbnails import CreateThumbnail
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class KindAnimal(CreateThumbnail, models.Model):
    """
    Справочник видов животных
    """
    kind = models.CharField(max_length=250, blank=False, null=False, verbose_name=_('Kind animal (dog, cat...)'))

    class Meta:
        verbose_name = _('Kind animal')
        verbose_name_plural = _('Kinds animals')

    def __str__(self):
        return self.kind


class KindAnimalAttr(models.Model):
    """
    Справочник характеристик видов животных
    """
    kind = models.ForeignKey(KindAnimal, on_delete=models.CASCADE, related_name='attrs', verbose_name=_('Kind animal'))
    attr = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('Name attr(weight, color...)'))

    class Meta:
        verbose_name = _('Kind attribute')
        verbose_name_plural = _('Kind attributes')

    def __str__(self):
       return self.kind.kind + ' - ' + self.attr
    #def __str__(self):
    #    return self.attr#self.kind.kind + self.attr


class KindAnimalAttrVal(models.Model):
    """
    Справочник значений характеристик видов животных
    """
    attr = models.ForeignKey(KindAnimalAttr, on_delete=models.CASCADE, related_name='attrvals', verbose_name=_('Kind animal attr'))
    value = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('attr val(blue, 40kg...)'))

    class Meta:
        verbose_name = _('Kind attribute value')
        verbose_name_plural = _('Kind attribute values')

    def __str__(self):
        return self.value#self.attr.kind.kind + self.attr.attr + self.value


class Animal(CreateThumbnail, models.Model):
    """
    Модель животного
    """
    user = models.ForeignKey(User, related_name='animals', on_delete=models.CASCADE, verbose_name=_('Owner'))
    first_name = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Имя'))
    second_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Кличка'))
    GENDER_CHOICES = (
        ('B', _('Мальчик')),
        ('G', _('Девочка')),
    )
    STATUS_CHOICES = (
        ('H', _('В поиске хозяина')),
        ('P', _('В поиске пары')),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True, verbose_name=_('Статус'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=True, verbose_name=_('Пол'))
    info = models.TextField(blank=True, null=True, verbose_name=_('О животном'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('Дата рождения'))
    kind = models.ForeignKey(KindAnimal, related_name='animals', verbose_name=_('Вид'),on_delete=models.CASCADE)
    avatar = models.ImageField(max_length=100, upload_to='animal/avatar', blank=True, null=True,
                               verbose_name=_('Аватар'))
    avatar_thumb = models.ImageField(max_length=100, upload_to='animal/avatar/thumbnail', blank=True, null=True)
    viewed = models.PositiveIntegerField(default=0, verbose_name=_('Viewed'))

    class Meta:
        verbose_name = _('Animal')
        verbose_name_plural = _('Animals')

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        try:
            this_record = Animal.objects.get(pk=self.pk)
            if this_record.avatar != self.avatar:
                this_record.avatar.delete(save=False)
                this_record.avatar_thumb.delete(save=False)
        except:
            pass

        self.create_thumbnail(width=300, height=300, from_img=self.avatar, to_img=self.avatar_thumb)

        force_update = False

        if self.id:
            force_update = True

        super(Animal, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.avatar.delete(save=False)
        self.avatar_thumb.delete(save=False)
        super(Animal, self).delete(*args, **kwargs)


class AnimalAttr(models.Model):
    """
    Характеристики животного
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='AnimalAttr', verbose_name=_('Animal'))
    kind = models.ForeignKey(KindAnimal, related_name='kinds', verbose_name=_('Kind animal'),on_delete=models.DO_NOTHING)
    attr = models.ForeignKey(KindAnimalAttr, related_name='attribues', verbose_name=_('Attributes'),on_delete=models.DO_NOTHING)
    value = models.ForeignKey(KindAnimalAttrVal, related_name='values', verbose_name=_('Attr animal value'),on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Animal attribute')
        verbose_name_plural = _('Animal attributes')

    def __str__(self):
        return self.animal.first_name + self.attr.attr + self.value.value



class AnimalPhoto(CreateThumbnail, models.Model):
    """
    Модель фото животного
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='AnimalPhoto', verbose_name=_('Animal'))
    title = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(max_length=100, upload_to='animal/photo', blank=False, null=False,
                               verbose_name=_('Фотография'))
    photo_thumb = models.ImageField(max_length=100, upload_to='animal/photo/thumbnail', blank=True, null=True)

    class Meta:
        verbose_name = _('AnimalPhoto')
        verbose_name_plural = _('AnimalPhotos')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        self.create_thumbnail(width=300, height=300, from_img=self.photo, to_img=self.photo_thumb)
        super(AnimalPhoto, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.photo.delete(save=False)
        self.photo_thumb.delete(save=False)
        super(AnimalPhoto, self).delete(*args, **kwargs)



class AnimalViewed(models.Model):
    """
    Модель для учета уникальных просмотров животного
    """
    profile_page = models.ForeignKey(User, on_delete=models.CASCADE, related_name='an_user_viewed', blank=False,
                                     verbose_name=_('Profile_page'))
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='animal_viewed', blank=False,
                             verbose_name=_('Animal'))

    class Meta:
        verbose_name = _('Animal Viewed')
        verbose_name_plural = _('Animals Viewed')

    def __str__(self):
        return '[' + self.profile_page.username + '] - ' + self.animal.first_name
