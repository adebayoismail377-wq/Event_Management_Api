from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls