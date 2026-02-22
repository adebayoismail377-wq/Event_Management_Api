from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls