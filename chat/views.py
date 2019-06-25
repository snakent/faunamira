from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from django.db.models import Q
from django.contrib.auth.models import User

@login_required
def index(request, open_chat=None):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    open_room = None
    chatuser = User.objects.filter(username=open_chat).first()
    if open_chat and chatuser:
        oldroom = rooms.filter(Q(user1=chatuser) | Q(user2=chatuser)).first()
        if oldroom:
            open_room = oldroom.pk
        else:
        #new room
            newroom = Room(user1=request.user, user2=chatuser)
            newroom.save()
            open_room = newroom.pk
            rooms = Room.objects.filter(Q(user1=request.user) | Q(user2=request.user))

    # Render that in the index template
    return render(request, "chat.html", {
        "rooms": rooms,
        "open_room" : open_room,
        "settitle" : 'Чат'
    }
)