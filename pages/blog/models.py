from django.db import models
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from dry_library.backend.thumbnails import CreateThumbnail
from pages.animal.models import Animal

class Blog(CreateThumbnail, models.Model):
    """
    Блог
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog', verbose_name=_('Author'))
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('Title'))
    article = tinymce_models.HTMLField(blank=False, null=False, verbose_name=_('Content'))
    date = models.DateTimeField(blank=False, null=False, verbose_name=_('Date of publication'))
    image = models.ImageField(max_length=100, upload_to='article', blank=True, null=True,verbose_name=_('Image'))
    image_thumb = models.ImageField(max_length=100, upload_to='article/thumbnail', blank=True, null=True)
    viewed = models.PositiveIntegerField(default=0, verbose_name=_('Viewed'))
    animals = models.ManyToManyField(Animal, blank=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = _('Blog')
        verbose_name_plural = _('Blog')

    def __str__(self):
         return (self.user.username) + ' ' + self.title

    def get_actual_articles(articles):
        act_articles = articles.filter(date__lte=timezone.now())
        return act_articles


    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        try:
            this_record = Blog.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
                this_record.image_thumb.delete(save=False)
        except:
            pass

        self.create_thumbnail(width=260, height=190, from_img=self.image, to_img=self.image_thumb)

        force_update = False

        if self.id:
            force_update = True

        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.image.delete(save=False)
        self.image_thumb.delete(save=False)
        super(Blog, self).delete(*args, **kwargs)


class BlogViewed(models.Model):
    """
    Модель для учета уникальных просмотров блога
    """
    blog_page = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_viewed', blank=False,
                                     verbose_name=_('Blog_page'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_user_viewed', blank=False,
                             verbose_name=_('User'))

    class Meta:
        verbose_name = _('Blog Viewed')
        verbose_name_plural = _('Blog Vieweds')

    def __str__(self):
        return '[' + self.blog_page.title + '] - ' + self.user.username
