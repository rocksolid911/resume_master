"""
Custom exception handler for DRF
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Log the error
        logger.error(
            f"API Error: {exc.__class__.__name__}: {str(exc)}",
            extra={'context': context}
        )

        # Customize the response format
        error_data = {
            'success': False,
            'error': {
                'message': str(exc),
                'type': exc.__class__.__name__,
            }
        }

        # Add field-specific errors if available
        if hasattr(response, 'data'):
            if isinstance(response.data, dict):
                error_data['error']['details'] = response.data
            else:
                error_data['error']['details'] = {'non_field_errors': response.data}

        response.data = error_data

    return response
