from django.contrib import admin
from django.urls import path
from rest_framework import routers

from blog.api import PostViewSet , ResponseViewSet , BulkCreateView

router = routers.DefaultRouter()

router.register(r"posts", PostViewSet , basename= "post")
router.register(r"response", ResponseViewSet , basename= "response")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/bulk_create', BulkCreateView.as_view() , name ="bulk"),
]+router.urls


