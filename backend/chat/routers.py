from django.urls import path

from rest_framework import routers

from .views import UserViewSet, ChatViewSet, ChatEnterListApiView

router = routers.DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"chat", ChatViewSet)
urlpatterns = router.urls
urlpatterns.append(path("chats/", ChatEnterListApiView.as_view()))
