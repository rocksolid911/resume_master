"""
AI Enhancement URLs
"""
from django.urls import path
from api.views import AIEnhanceView, AISuggestImprovementsView, AIEnhancementAcceptView

urlpatterns = [
    path('enhance-text/', AIEnhanceView.as_view(), name='enhance-text'),
    path('suggest-improvements/', AISuggestImprovementsView.as_view(), name='suggest-improvements'),
    path('enhancements/<int:enhancement_id>/accept/', AIEnhancementAcceptView.as_view(), name='accept-enhancement'),
]
