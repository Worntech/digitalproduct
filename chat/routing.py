from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<unique_code>\w+)/$", ChatConsumer.as_asgi()),  # ✅ Match unique_code
]