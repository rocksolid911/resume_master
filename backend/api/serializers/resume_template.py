"""
Resume Template Serializers
"""
from rest_framework import serializers
from api.models import ResumeTemplate


class ResumeTemplateListSerializer(serializers.ModelSerializer):
    """Serializer for template list view (minimal data)"""

    class Meta:
        model = ResumeTemplate
        fields = [
            'id',
            'template_id',
            'name',
            'description',
            'category',
            'preview_image',
            'thumbnail',
            'is_premium',
            'supports_photo',
            'supports_colors',
            'usage_count',
            'rating',
        ]
        read_only_fields = fields


class ResumeTemplateSerializer(serializers.ModelSerializer):
    """Detailed serializer for template details"""

    class Meta:
        model = ResumeTemplate
        fields = [
            'id',
            'template_id',
            'name',
            'description',
            'category',
            'html_structure',
            'css_styling',
            'preview_image',
            'thumbnail',
            'is_active',
            'is_premium',
            'supports_photo',
            'supports_colors',
            'usage_count',
            'rating',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'usage_count',
            'rating',
            'created_at',
            'updated_at',
        ]
