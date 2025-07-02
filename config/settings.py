"""
Professional Configuration Settings for Resume Analysis Application

This module contains comprehensive configuration settings for the enterprise-grade
resume analysis application. Provides centralized configuration management for
application behavior, AI models, processing parameters, and UI theming.

Configuration Categories:
    - APPLICATION_CONFIG: Core application settings and metadata
    - AI_MODEL_CONFIG: Machine learning and AI processing parameters
    - FILE_PROCESSING_CONFIG: Document handling and validation settings
    - COST_ESTIMATION_CONFIG: API usage and cost calculation parameters
    - UI_THEME_CONFIG: Professional styling and color scheme settings

Author: Resume Analysis Team
Version: 1.0.0
"""
import os
from typing import Dict, Any, Optional

# Core Application Configuration
APPLICATION_CONFIG = {
    "title": "Professional Resume Analysis Platform",
    "layout": "wide",
    "page_icon": "🔍",
    "initial_sidebar_state": "expanded",
    "app_version": "1.0.0",
    "environment": os.getenv("APP_ENVIRONMENT", "production")
}

# AI and Machine Learning Model Configuration
AI_MODEL_CONFIG = {
    "primary_gpt_model": "gpt-4o",
    "processing_temperature": 0.1,  # Low temperature for consistent, factual output
    "max_response_tokens": 2000,
    "semantic_matching_threshold": 0.75,  # Higher threshold for better precision
    "sentence_transformer_model": "all-MiniLM-L6-v2",
    "enable_cost_optimization": True,
    "retry_attempts": 3
}

# Document Processing and Validation Configuration
FILE_PROCESSING_CONFIG = {
    "maximum_file_size_bytes": 15 * 1024 * 1024,  # 15MB for professional documents
    "supported_file_formats": [".pdf"],
    "text_extraction_methods": ["pymupdf", "optical_character_recognition"],
    "minimum_text_length": 100,  # Minimum viable document length
    "enable_content_validation": True
}

# Cost Estimation and API Usage Configuration
COST_ESTIMATION_CONFIG = {
    "gpt4o_input_cost_per_1k_tokens": 0.005,
    "gpt4o_output_cost_per_1k_tokens": 0.015,
    "gpt4o_input_rate": 0.005,  # Cost per 1K input tokens
    "gpt4o_output_rate": 0.015,  # Cost per 1K output tokens
    "enable_cost_tracking": True,
    "cost_alert_threshold": 10.0,  # Alert if analysis costs exceed $10
    "batch_processing_discount": 0.1  # 10% discount for bulk operations
}

# Professional UI Theme and Styling Configuration
UI_THEME_CONFIG = {
    "primary_brand_color": "#1976d2",      # Professional blue
    "secondary_accent_color": "#00acc1",   # Complementary teal
    "success_indicator_color": "#388e3c",  # Green for positive results
    "warning_indicator_color": "#f57c00",  # Orange for attention items
    "error_indicator_color": "#d32f2f",    # Red for issues
    "info_highlight_color": "#1976d2",     # Blue for information
    "background_gradient": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
    "card_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "border_radius": "8px",
    "font_family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
}

def get_openai_api_key() -> Optional[str]:
    """
    Retrieve OpenAI API key from environment variables with validation.
    
    Returns:
        OpenAI API key if available, None otherwise
        
    Raises:
        EnvironmentError: If API key is not configured in production environment
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key and APPLICATION_CONFIG["environment"] == "production":
        raise EnvironmentError(
            "OpenAI API key is required for production environment. "
            "Please set the OPENAI_API_KEY environment variable."
        )
    
    return api_key


def validate_configuration() -> bool:
    """
    Validate all configuration settings for consistency and completeness.
    
    Returns:
        True if all configurations are valid, False otherwise
    """
    try:
        # Validate AI model configuration
        if AI_MODEL_CONFIG["processing_temperature"] < 0 or AI_MODEL_CONFIG["processing_temperature"] > 2:
            return False
            
        # Validate file processing limits
        if FILE_PROCESSING_CONFIG["maximum_file_size_bytes"] <= 0:
            return False
            
        # Validate cost thresholds
        if COST_ESTIMATION_CONFIG["cost_alert_threshold"] <= 0:
            return False
            
        return True
        
    except (KeyError, TypeError):
        return False


# Legacy compatibility mappings for existing code
APP_CONFIG = APPLICATION_CONFIG
AI_CONFIG = AI_MODEL_CONFIG  
FILE_CONFIG = FILE_PROCESSING_CONFIG
COST_CONFIG = COST_ESTIMATION_CONFIG
THEME_CONFIG = UI_THEME_CONFIG

def validate_config() -> bool:
    """Validate that all necessary configurations are set."""
    if not get_openai_api_key():
        return False
    return True
