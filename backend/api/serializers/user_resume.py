"""
User Resume Serializers
"""
from rest_framework import serializers
from api.models import UserResume, ResumeTemplate
from .resume_template import ResumeTemplateListSerializer


class UserResumeListSerializer(serializers.ModelSerializer):
    """Serializer for resume list view"""

    template_name = serializers.CharField(source='template.name', read_only=True)
    template_category = serializers.CharField(source='template.category', read_only=True)

    class Meta:
        model = UserResume
        fields = [
            'id',
            'title',
            'template_name',
            'template_category',
            'is_active',
            'is_public',
            'public_slug',
            'view_count',
            'download_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class UserResumeSerializer(serializers.ModelSerializer):
    """Detailed serializer for resume"""

    template_details = ResumeTemplateListSerializer(source='template', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserResume
        fields = [
            'id',
            'user_email',
            'template',
            'template_details',
            'title',
            'resume_data_json',
            'custom_colors',
            'custom_fonts',
            'is_active',
            'is_public',
            'public_slug',
            'pdf_file',
            'docx_file',
            'view_count',
            'download_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user_email',
            'public_slug',
            'pdf_file',
            'docx_file',
            'view_count',
            'download_count',
            'created_at',
            'updated_at',
        ]

    def validate_resume_data_json(self, value):
        """Validate resume data structure"""
        required_fields = ['personal_info']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(
                    f"Resume data must contain '{field}' field"
                )
        return value


class UserResumeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new resume"""

    class Meta:
        model = UserResume
        fields = [
            'template',
            'title',
            'resume_data_json',
            'custom_colors',
            'custom_fonts',
        ]

    def validate_template(self, value):
        """Validate template exists and is active"""
        if not value.is_active:
            raise serializers.ValidationError("This template is not available")
        return value

    def create(self, validated_data):
        """Create resume with current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
