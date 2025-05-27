# paypay_backend/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from billing.routing import websocket_urlpatterns 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paypay_backend.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 处理 HTTP 请求（和原来的 wsgi 一样）
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # WebSocket 请求走这里
    ),
})
