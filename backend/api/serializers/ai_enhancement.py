"""
AI Enhancement Serializers
"""
from rest_framework import serializers
from api.models import AIEnhancement


class AIEnhanceRequestSerializer(serializers.Serializer):
    """Serializer for AI enhancement request"""

    text = serializers.CharField(
        required=True,
        help_text="Text to enhance"
    )
    section_type = serializers.CharField(
        required=True,
        help_text="Type of section (experience, education, skills, etc.)"
    )
    enhancement_type = serializers.ChoiceField(
        choices=[
            ('bullet_point', 'Bullet Point Enhancement'),
            ('description', 'Description Enhancement'),
            ('summary', 'Summary Generation'),
            ('grammar', 'Grammar & Style Improvement'),
            ('keywords', 'Keyword Optimization'),
            ('full_rewrite', 'Full Section Rewrite'),
        ],
        default='bullet_point',
        help_text="Type of enhancement to perform"
    )
    resume_id = serializers.IntegerField(
        required=False,
        help_text="Resume ID (optional)"
    )
    context = serializers.DictField(
        required=False,
        help_text="Additional context for enhancement (job title, industry, etc.)"
    )

    def validate_text(self, value):
        """Validate text length"""
        if len(value) < 10:
            raise serializers.ValidationError("Text must be at least 10 characters long")
        if len(value) > 5000:
            raise serializers.ValidationError("Text must not exceed 5000 characters")
        return value


class AIEnhancementSerializer(serializers.ModelSerializer):
    """Serializer for AI enhancement records"""

    class Meta:
        model = AIEnhancement
        fields = [
            'id',
            'section_type',
            'enhancement_type',
            'original_text',
            'enhanced_text',
            'confidence_score',
            'model_used',
            'was_accepted',
            'user_feedback',
            'created_at',
            'accepted_at',
        ]
        read_only_fields = fields


class AIEnhancementResponseSerializer(serializers.Serializer):
    """Serializer for AI enhancement response"""

    enhanced_text = serializers.CharField()
    original_text = serializers.CharField()
    confidence_score = serializers.FloatField()
    suggestions = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    improvement_metrics = serializers.DictField(required=False)
    enhancement_id = serializers.IntegerField()
