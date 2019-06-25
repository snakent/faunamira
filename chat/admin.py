from django.contrib import admin
from chat.models import Room, Message

'''
admin.site.register(
    Room,
    list_display=["id",  "user1", "user2"],
    list_display_links=["id", ],
)
'''

admin.site.register(
    Message,
    list_display=["dialog",  "user", "message", "date"],
    list_display_links=["dialog", ],
)