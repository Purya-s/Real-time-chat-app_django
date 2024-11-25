#This will route the WebSocket connections to the consumers.

from django.urls import path , include 
from . import consumers

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    path('ws/<str:room_name>/' , consumers.ChatConsumer.as_asgi()), 
] 