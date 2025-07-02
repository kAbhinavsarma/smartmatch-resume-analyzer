"""
Professional GPT-4 Handlers for Resume and Job Description Analysis

This module provides enterprise-grade AI-powered skill extraction and analysis
capabilities using OpenAI's GPT-4 model. Designed for production use in
recruitment and talent acquisition workflows.

Functions:
    - extract_job_description_skills: Extract and categorize skills from job descriptions
    - extract_resume_skills: Extract and categorize skills from resumes  
    - generate_skill_summary: Generate professional candidate summaries
    - analyze_job_requirements: Analyze and summarize job requirements
    - recommend_skill_improvement: Provide skill gap recommendations

Author: Resume Analysis Team
Version: 1.0.0
"""
import openai
import os
import re
import json
import logging
from typing import Dict, Any, Optional, List

# Configure logging for production monitoring
logger = logging.getLogger(__name__)

class OpenAIClientManager:
    """Manages OpenAI API client initialization and configuration."""
    
    @staticmethod
    def get_client(api_key: Optional[str] = None) -> openai.OpenAI:
        """
        Initialize and return OpenAI client with proper error handling.
        
        Args:
            api_key: Optional OpenAI API key. Uses environment variable if not provided.
            
        Returns:
            Configured OpenAI client instance
            
        Raises:
            ValueError: If API key is not provided or found in environment
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise ValueError("OpenAI API key not set. Please configure OPENAI_API_KEY environment variable.")
        
        return openai.OpenAI(api_key=api_key)

def extract_job_description_skills(jd_text: str, openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract and categorize skills from job description using GPT-4.
    
    Args:
        jd_text: Job description text to analyze
        openai_api_key: Optional OpenAI API key
        
    Returns:
        Dictionary mapping skill names to their metadata (category, importance, must_have)
    """
    try:
        client = OpenAIClientManager.get_client(openai_api_key)
        
        # Truncate text to manageable size for API processing
        processed_text = jd_text[:2000]
        
        # Professional skill categories for enterprise analysis
        skill_categories = [
            "Programming Languages", "Frameworks & Libraries", "Development Tools", 
            "Databases", "Cloud Platforms", "Technical Concepts", "Professional Skills"
        ]
        
        prompt = (
            "As an expert technical recruiter, extract all required skills from this job description. "
            f"Categorize each skill into one of: {skill_categories}. "
            "For each skill, provide: skill name, category, "
            "importance level (Critical/High/Medium/Low), and must_have status (true/false). "
            "Return only a well-formatted JSON object:\n"
            '{ "skill_name": { "category": "Programming Languages", "importance": "Critical", "must_have": true } }\n\n'
            f"Job Description:\n{processed_text}\n\nResponse (JSON only):"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter with deep knowledge of industry skill requirements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for consistent, factual extraction
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content
        logger.info(f"GPT-4 job description analysis completed successfully")
        
        # Extract JSON from response with robust parsing
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            logger.warning("No valid JSON structure found in GPT-4 response")
            return {}
            
        return json.loads(json_match.group())
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in job description skill extraction: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error during job description skill extraction: {e}")
        return {}

def extract_resume_skills(resume_text: str, openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract and categorize skills from resume using GPT-4.
    
    Args:
        resume_text: Resume text to analyze
        openai_api_key: Optional OpenAI API key
        
    Returns:
        Dictionary mapping skill names to their metadata (category, importance)
    """
    try:
        client = OpenAIClientManager.get_client(openai_api_key)
        
        # Truncate text for optimal API processing
        processed_text = resume_text[:3000]
        
        # Professional skill categories for comprehensive analysis
        skill_categories = [
            "Programming Languages", "Frameworks & Libraries", "Development Tools", 
            "Databases", "Cloud Platforms", "Technical Concepts", "Professional Skills"
        ]
        
        prompt = (
            "As an expert technical recruiter, extract all skills demonstrated in this resume. "
            f"Categorize each skill into one of: {skill_categories}. "
            "For each skill, provide: skill name, category, and "
            "proficiency level (Expert/Advanced/Intermediate/Basic). "
            "Return only a well-formatted JSON object:\n"
            '{ "skill_name": { "category": "Programming Languages", "proficiency": "Advanced" } }\n\n'
            f"Resume:\n{processed_text}\n\nResponse (JSON only):"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter with deep knowledge of candidate skill assessment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for consistent skill identification
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content
        logger.info(f"GPT-4 resume analysis completed successfully")
        
        # Extract JSON from response with robust parsing
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            logger.warning("No valid JSON structure found in GPT-4 response")
            return {}
            
        return json.loads(json_match.group())
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in resume skill extraction: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error during resume skill extraction: {e}")
        return {}

def generate_skill_summary(resume_text: str, skill_data: Dict[str, Any]) -> str:
    """
    Generate a professional candidate summary based on resume and extracted skills.
    
    Args:
        resume_text: Original resume text
        skill_data: Extracted skills with metadata
        
    Returns:
        Professional candidate summary string
    """
    try:
        client = OpenAIClientManager.get_client()
        
        # Truncate resume text for processing efficiency
        processed_text = resume_text[:1000]
        
        prompt = (
            "Based on the following resume and extracted skill analysis, "
            "write a professional 2-3 sentence executive summary highlighting the candidate's "
            "key technical strengths, experience level, and primary areas of expertise. "
            "Focus on concrete skills and measurable capabilities.\n\n"
            f"Resume Content:\n{processed_text}\n\n"
            f"Skill Analysis:\n{json.dumps(skill_data, indent=2)}\n\n"
            "Professional Executive Summary:"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert executive recruiter specializing in technical talent assessment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Slightly higher for natural language generation
            max_tokens=2000
        )
        
        summary = response.choices[0].message.content.strip()
        logger.info("Professional candidate summary generated successfully")
        return summary
        
    except Exception as e:
        logger.error(f"Error generating candidate summary: {e}")
        return "Professional summary could not be generated due to processing constraints."

def analyze_job_requirements(jd_text: str, skill_data: Dict[str, Any]) -> str:
    """
    Generate comprehensive analysis of job description requirements and priorities.
    
    Args:
        jd_text: Job description text
        skill_data: Extracted skills with metadata
        
    Returns:
        Professional analysis of job requirements and key focus areas
    """
    try:
        client = OpenAIClientManager.get_client()
        
        prompt = (
            "Given the following job description and extracted skill requirements, "
            "provide a concise professional analysis (2-3 sentences) highlighting: "
            "1) The most critical technical requirements, "
            "2) Must-have vs nice-to-have skills, and "
            "3) The overall technical focus and seniority level expected.\n\n"
            f"Job Description:\n{jd_text}\n\n"
            f"Extracted Skill Requirements:\n{json.dumps(skill_data, indent=2)}\n\n"
            "Requirements Analysis:"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter specializing in job requirement analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content.strip()
        logger.info("Job requirements analysis completed successfully")
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing job requirements: {e}")
        return "Job requirements analysis could not be completed due to processing constraints."


def recommend_skill_improvement(resume_skills: Dict[str, Any], jd_skills: Dict[str, Any], 
                              missing_skills: List[str]) -> str:
    """
    Generate targeted skill improvement recommendations for candidate development.
    
    Args:
        resume_skills: Candidate's current skills with metadata
        jd_skills: Job requirements with metadata
        missing_skills: List of skills missing from candidate's profile
        
    Returns:
        Professional skill development recommendations
    """
    try:
        client = OpenAIClientManager.get_client()
        
        prompt = (
            "As a technical career advisor, provide specific, actionable skill development "
            "recommendations for this candidate based on their current skills and job requirements. "
            "Focus on the most impactful skills to learn and suggest learning priorities. "
            "Provide 2-3 concrete recommendations with brief rationale.\n\n"
            f"Current Candidate Skills:\n{json.dumps(resume_skills, indent=2)}\n\n"
            f"Job Requirements:\n{json.dumps(jd_skills, indent=2)}\n\n"
            f"Skills Gap Identified:\n{missing_skills}\n\n"
            "Development Recommendations:"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert technical career advisor with deep knowledge of skill development pathways."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Slightly higher for creative recommendations
            max_tokens=2000
        )
        
        recommendations = response.choices[0].message.content.strip()
        logger.info("Skill improvement recommendations generated successfully")
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating skill recommendations: {e}")
        return "Skill development recommendations could not be generated due to processing constraints."


# Legacy function mappings for backward compatibility
def gpt_extract_jd_skills(jd_text: str, openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """Legacy function - use extract_job_description_skills instead."""
    return extract_job_description_skills(jd_text, openai_api_key)


def gpt_extract_resume_skills(resume_text: str, openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """Legacy function - use extract_resume_skills instead."""
    return extract_resume_skills(resume_text, openai_api_key)


def gpt_skill_summary(resume_text: str, skill_json: Dict[str, Any]) -> str:
    """Legacy function - use generate_skill_summary instead."""
    return generate_skill_summary(resume_text, skill_json)


def gpt_jd_insight(jd_text: str, skill_json: Dict[str, Any]) -> str:
    """Legacy function - use analyze_job_requirements instead."""
    return analyze_job_requirements(jd_text, skill_json)

# --- Skill Recommendation ---
def gpt_skill_recommendation(skill, jd_text=""):
    """Generate learning recommendation for a specific skill."""
    client = OpenAIClientManager.get_client()
    prompt = (
        f"Suggest a concise, actionable way for a candidate to learn or demonstrate the skill '{skill}'. "
        "Provide specific, practical recommendations. Keep it under 200 words and ensure you complete all points without cutoff. "
        "Focus on 2-3 key actionable steps."
    )
    if jd_text:
        prompt += f" The job description context is: {jd_text[:500]}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert career coach. Provide complete, actionable recommendations without cutoff."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # Reduced from 2000 to 300
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating skill recommendation: {e}")
        return "No recommendation available."

# Alias for backward compatibility
def get_single_skill_recommendation(skill, jd_text=""):
    """Get recommendation for a single skill (legacy compatibility)."""
    return gpt_skill_recommendation(skill, jd_text)

# --- Comprehensive AI Skill Gap Analysis ---
def generate_comprehensive_analysis(prompt: str, openai_api_key: Optional[str] = None) -> str:
    """
    Generate a comprehensive skill gap analysis using GPT-4o.
    Args:
        prompt: The prompt describing the skill gap analysis task
        openai_api_key: Optional API key override
    Returns:
        AI-generated analysis string
    """
    try:
        client = OpenAIClientManager.get_client(openai_api_key)
        
        # Enhanced prompt to prevent cutoffs
        enhanced_prompt = (
            f"{prompt}\n\n"
            "IMPORTANT: Keep your response under 400 words and ensure you complete all points without cutoff. "
            "Provide 3-4 key actionable recommendations with brief explanations."
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional HR analyst and career coach. Provide detailed, actionable, and recruiter-focused skill gap analysis. Always complete your responses without cutoff."},
                {"role": "user", "content": enhanced_prompt}
            ],
            max_tokens=600,  # Reduced from 1800 to 600
            temperature=0.6,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating comprehensive skill gap analysis: {e}")
        return "Comprehensive skill gap analysis could not be generated at this time."
