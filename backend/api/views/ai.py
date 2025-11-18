"""
AI Enhancement Views
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from api.models import AIEnhancement, UserResume
from api.serializers import (
    AIEnhanceRequestSerializer,
    AIEnhancementResponseSerializer
)
from api.services import AIService
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AIEnhanceView(APIView):
    """
    AI text enhancement endpoint
    POST /api/ai/enhance-text/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validate request data
        serializer = AIEnhanceRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'error': {
                    'message': 'Invalid request data',
                    'type': 'ValidationError',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Check if user can use AI enhancement
        user = request.user
        if not user.can_use_ai_enhancement():
            return Response({
                'success': False,
                'error': {
                    'message': f'Daily AI enhancement limit reached. '
                               f'You have used {user.ai_enhancements_used_today} enhancements today.',
                    'type': 'RateLimitError',
                    'details': {
                        'limit': settings.AI_ENHANCEMENT_RATE_LIMIT,
                        'used': user.ai_enhancements_used_today,
                        'subscription_tier': user.subscription_tier
                    }
                }
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            # Initialize AI service
            ai_service = AIService()

            # Enhance text
            enhanced_text, confidence_score, prompt_tokens, completion_tokens = ai_service.enhance_text(
                text=data['text'],
                section_type=data['section_type'],
                enhancement_type=data['enhancement_type'],
                context=data.get('context', {})
            )

            # Get resume if provided
            resume = None
            if data.get('resume_id'):
                try:
                    resume = UserResume.objects.get(id=data['resume_id'], user=user)
                except UserResume.DoesNotExist:
                    pass

            # Save enhancement record
            enhancement = AIEnhancement.objects.create(
                user=user,
                resume=resume,
                section_type=data['section_type'],
                enhancement_type=data['enhancement_type'],
                original_text=data['text'],
                enhanced_text=enhanced_text,
                confidence_score=confidence_score,
                model_used=ai_service.model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            # Increment user's AI usage counter
            user.increment_ai_usage()

            # Calculate improvement metrics
            improvement_metrics = {
                'original_length': len(data['text']),
                'enhanced_length': len(enhanced_text),
                'word_count_change': len(enhanced_text.split()) - len(data['text'].split()),
            }

            logger.info(
                f"AI enhancement successful for user {user.email}: "
                f"{data['enhancement_type']} on {data['section_type']}"
            )

            response_data = {
                'enhanced_text': enhanced_text,
                'original_text': data['text'],
                'confidence_score': confidence_score,
                'improvement_metrics': improvement_metrics,
                'enhancement_id': enhancement.id,
                'suggestions': []
            }

            return Response({
                'success': True,
                'message': 'Text enhanced successfully',
                'data': response_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"AI enhancement failed: {str(e)}")
            return Response({
                'success': False,
                'error': {
                    'message': 'AI enhancement failed. Please try again.',
                    'type': 'AIServiceError',
                    'details': str(e) if settings.DEBUG else None
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AISuggestImprovementsView(APIView):
    """
    AI resume improvement suggestions endpoint
    POST /api/ai/suggest-improvements/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        resume_id = request.data.get('resume_id')

        if not resume_id:
            return Response({
                'success': False,
                'error': {
                    'message': 'resume_id is required',
                    'type': 'ValidationError'
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get resume
        try:
            resume = UserResume.objects.get(id=resume_id, user=request.user)
        except UserResume.DoesNotExist:
            return Response({
                'success': False,
                'error': {
                    'message': 'Resume not found',
                    'type': 'NotFoundError'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        # Check AI usage limit
        user = request.user
        if not user.can_use_ai_enhancement():
            return Response({
                'success': False,
                'error': {
                    'message': 'Daily AI enhancement limit reached',
                    'type': 'RateLimitError'
                }
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            # Initialize AI service
            ai_service = AIService()

            # Get suggestions
            suggestions = ai_service.suggest_improvements(resume.resume_data_json)

            # Increment user's AI usage counter (this counts as 1 enhancement)
            user.increment_ai_usage()

            logger.info(f"Resume analysis completed for resume {resume_id}")

            return Response({
                'success': True,
                'message': 'Resume analyzed successfully',
                'data': suggestions
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Resume analysis failed: {str(e)}")
            return Response({
                'success': False,
                'error': {
                    'message': 'Resume analysis failed. Please try again.',
                    'type': 'AIServiceError',
                    'details': str(e) if settings.DEBUG else None
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIEnhancementAcceptView(APIView):
    """
    Accept AI enhancement
    POST /api/ai/enhancements/{id}/accept/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, enhancement_id, *args, **kwargs):
        try:
            enhancement = AIEnhancement.objects.get(
                id=enhancement_id,
                user=request.user
            )
        except AIEnhancement.DoesNotExist:
            return Response({
                'success': False,
                'error': {
                    'message': 'Enhancement not found',
                    'type': 'NotFoundError'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        # Mark as accepted
        enhancement.accept()

        # Optional: save feedback
        feedback = request.data.get('feedback')
        if feedback in ['excellent', 'good', 'average', 'poor']:
            enhancement.user_feedback = feedback
            enhancement.save()

        logger.info(f"Enhancement {enhancement_id} accepted by user {request.user.email}")

        return Response({
            'success': True,
            'message': 'Enhancement accepted'
        })
