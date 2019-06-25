from channels.db import database_sync_to_async

from chat.exceptions import ClientError
from .models import Room, Message

# Serialize querysets
from django.core import serializers

# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    if room.user1 != user and room.user2 != user:
        raise ClientError("ROOM_NOT_FOR_YOU")
    return room


@database_sync_to_async
def new_message(room_id, user, message):
    """
    Add new message to db.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        #add message to log
        msg_room = Room.objects.filter(pk=room_id).first()
        msg = Message(dialog=msg_room, user=user, message=message)
        msg.save()
    except:
        raise ClientError("NEW MESSAGE DB ERROR")
    return msg


@database_sync_to_async
def get_history_json(room, start=0, offset=20):
    """
    Get history
    """
    try:
        history = Message.objects.filter(dialog = room.pk).order_by('-id')[start:start+offset][::-1]
        history = serializers.serialize('json', history)
    except:
        raise ClientError("CANT GET HISTORY")
    return history
