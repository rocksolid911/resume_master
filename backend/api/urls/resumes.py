"""
Resume URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserResumeViewSet

router = DefaultRouter()
router.register(r'', UserResumeViewSet, basename='resume')

urlpatterns = [
    path('', include(router.urls)),
]
