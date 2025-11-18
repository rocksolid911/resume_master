"""
Resume Section Serializers
"""
from rest_framework import serializers
from api.models import ResumeSection


class ResumeSectionSerializer(serializers.ModelSerializer):
    """Serializer for resume sections"""

    class Meta:
        model = ResumeSection
        fields = [
            'id',
            'resume',
            'section_type',
            'section_title',
            'content',
            'order',
            'is_visible',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate section belongs to user's resume"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            resume = attrs.get('resume', self.instance.resume if self.instance else None)
            if resume and resume.user != request.user:
                raise serializers.ValidationError("You can only modify your own resume sections")
        return attrs
