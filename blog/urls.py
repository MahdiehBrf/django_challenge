from rest_framework import routers

from .api import PostViewSet, ResponseViewSet

app_name = 'posts'

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'response', ResponseViewSet, basename='response')
urlpatterns = router.urls
