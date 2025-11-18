"""
Resume Template Views
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from api.models import ResumeTemplate
from api.serializers import ResumeTemplateSerializer, ResumeTemplateListSerializer
import logging

logger = logging.getLogger(__name__)


class ResumeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for resume templates
    GET /api/templates/ - List all templates
    GET /api/templates/{id}/ - Get template details
    """
    queryset = ResumeTemplate.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ResumeTemplateListSerializer
        return ResumeTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Filter by premium status
        premium = self.request.query_params.get('premium', None)
        if premium is not None:
            is_premium = premium.lower() == 'true'
            queryset = queryset.filter(is_premium=is_premium)

        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # Sort options
        sort = self.request.query_params.get('sort', '-usage_count')
        if sort in ['usage_count', '-usage_count', 'name', '-name', 'rating', '-rating']:
            queryset = queryset.order_by(sort)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': {
                'count': queryset.count(),
                'templates': serializer.data
            }
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'success': True,
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of available categories"""
        categories = [
            {'value': cat[0], 'label': cat[1]}
            for cat in ResumeTemplate.TEMPLATE_CATEGORIES
        ]

        return Response({
            'success': True,
            'data': categories
        })
