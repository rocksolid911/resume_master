"""
AI Service for resume enhancement using OpenAI
"""
import openai
from django.conf import settings
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered resume enhancements"""

    def __init__(self):
        """Initialize OpenAI client"""
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"

    def enhance_text(
        self,
        text: str,
        section_type: str,
        enhancement_type: str,
        context: Dict = None
    ) -> Tuple[str, float, int, int]:
        """
        Enhance resume text using AI

        Args:
            text: Original text to enhance
            section_type: Type of section (experience, education, etc.)
            enhancement_type: Type of enhancement to perform
            context: Additional context (job title, industry, etc.)

        Returns:
            Tuple of (enhanced_text, confidence_score, prompt_tokens, completion_tokens)
        """
        try:
            # Build the prompt based on enhancement type
            prompt = self._build_prompt(text, section_type, enhancement_type, context)

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume writer and career coach. "
                                   "Your goal is to enhance resume content to be more impactful, "
                                   "professional, and achievement-focused. Use strong action verbs "
                                   "and quantify achievements when possible."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )

            # Extract enhanced text
            enhanced_text = response.choices[0].message.content.strip()

            # Calculate confidence score based on token usage and finish reason
            confidence_score = self._calculate_confidence(response)

            # Get token usage
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens

            logger.info(
                f"AI Enhancement successful: {section_type}/{enhancement_type}, "
                f"tokens: {prompt_tokens + completion_tokens}"
            )

            return enhanced_text, confidence_score, prompt_tokens, completion_tokens

        except Exception as e:
            logger.error(f"AI Enhancement failed: {str(e)}")
            raise

    def _build_prompt(
        self,
        text: str,
        section_type: str,
        enhancement_type: str,
        context: Dict = None
    ) -> str:
        """Build the appropriate prompt based on enhancement type"""

        context_info = ""
        if context:
            if 'job_title' in context:
                context_info += f"\nJob Title: {context['job_title']}"
            if 'industry' in context:
                context_info += f"\nIndustry: {context['industry']}"
            if 'years_experience' in context:
                context_info += f"\nYears of Experience: {context['years_experience']}"

        prompts = {
            'bullet_point': f"""
Enhance this resume bullet point to be more impactful and achievement-focused.
Use strong action verbs, quantify results where possible, and highlight the impact.
{context_info}

Original bullet point:
{text}

Provide ONLY the enhanced bullet point, nothing else.
""",
            'description': f"""
Improve this job/project description to be more professional and compelling.
Focus on responsibilities, achievements, and impact.
{context_info}

Original description:
{text}

Provide ONLY the enhanced description, nothing else.
""",
            'summary': f"""
Create a professional summary based on the following information.
Make it compelling, achievement-focused, and tailored to the target role.
{context_info}

Information:
{text}

Provide ONLY the professional summary (2-3 sentences), nothing else.
""",
            'grammar': f"""
Improve the grammar, style, and professionalism of this text while maintaining its meaning.
{context_info}

Original text:
{text}

Provide ONLY the corrected text, nothing else.
""",
            'keywords': f"""
Optimize this text for ATS (Applicant Tracking Systems) by adding relevant keywords
and industry-specific terminology while keeping it natural and readable.
{context_info}

Original text:
{text}

Provide ONLY the optimized text, nothing else.
""",
            'full_rewrite': f"""
Completely rewrite this {section_type} section to be more professional, impactful,
and achievement-focused. Use strong action verbs and quantify results.
{context_info}

Original text:
{text}

Provide ONLY the rewritten text, nothing else.
""",
        }

        return prompts.get(enhancement_type, prompts['bullet_point'])

    def _calculate_confidence(self, response) -> float:
        """
        Calculate confidence score based on API response

        Returns a score between 0 and 1
        """
        # Start with base confidence
        confidence = 0.8

        # Adjust based on finish reason
        finish_reason = response.choices[0].finish_reason
        if finish_reason == 'stop':
            confidence += 0.2
        elif finish_reason == 'length':
            confidence -= 0.1

        # Normalize to 0-1 range
        return max(0.0, min(1.0, confidence))

    def suggest_improvements(self, resume_data: Dict) -> Dict:
        """
        Analyze entire resume and suggest improvements

        Args:
            resume_data: Complete resume data JSON

        Returns:
            Dictionary with improvement suggestions
        """
        try:
            # Build analysis prompt
            prompt = f"""
Analyze this resume and provide specific, actionable suggestions for improvement.
Focus on:
1. Content strength and impact
2. ATS optimization
3. Formatting and structure
4. Keyword usage
5. Achievement quantification

Resume data:
{resume_data}

Provide your suggestions in this exact JSON format:
{{
    "overall_score": <score from 1-10>,
    "strengths": [<list of 3-5 strengths>],
    "improvements": [<list of 5-8 specific improvements>],
    "missing_sections": [<list of recommended sections to add>],
    "keyword_suggestions": [<list of relevant keywords to include>]
}}
"""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume analyst and career coach."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            # Parse and return suggestions
            import json
            suggestions_text = response.choices[0].message.content.strip()

            # Try to extract JSON from response
            try:
                # Find JSON in the response
                start_idx = suggestions_text.find('{')
                end_idx = suggestions_text.rfind('}') + 1
                json_str = suggestions_text[start_idx:end_idx]
                suggestions = json.loads(json_str)
            except:
                # Fallback to simple structure
                suggestions = {
                    "overall_score": 7,
                    "strengths": ["Resume content provided"],
                    "improvements": [suggestions_text],
                    "missing_sections": [],
                    "keyword_suggestions": []
                }

            logger.info("Resume analysis completed successfully")
            return suggestions

        except Exception as e:
            logger.error(f"Resume analysis failed: {str(e)}")
            raise
