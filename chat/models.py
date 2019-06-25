from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Room(models.Model):
    """
    A room for people to chat in.
    """
    user1 = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='user1', verbose_name=_('User1'))
    user2 = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='user2', verbose_name=_('User2'))


    def __str__(self):
        return self.user1.username + ' - ' + self.user2.username

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id


class Message(models.Model):
    """
    Модель сообщение
    """
    dialog = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE, verbose_name=_('Dialog'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',
                                  verbose_name=_('User'))
    message = models.TextField(verbose_name=_('Message'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-date']

    def __str__(self):
        return self.user.username + ' - ' + str(self.date)
