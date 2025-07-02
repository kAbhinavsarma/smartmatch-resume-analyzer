"""
Data models and type definitions for the application.
"""
from dataclasses import dataclass
from typing import Set, Dict, Any, Optional
from enum import Enum

class SkillImportance(Enum):
    """Enumeration for skill importance levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class ExtractionMethod(Enum):
    """Enumeration for skill extraction methods."""
    AI_GPT = "AI (GPT-4)"
    NLP_SPACY = "Modern NLP"

@dataclass
class SkillInfo:
    """Data class for skill information."""
    name: str
    category: str
    importance: SkillImportance
    must_have: bool = False

@dataclass
class ExtractionResult:
    """Data class for skill extraction results."""
    skills: Set[str]
    metadata: Dict[str, Any]
    extraction_time: float
    method: ExtractionMethod
    cost: Optional[str] = None

@dataclass
class MatchResult:
    """Data class for skill matching results."""
    matched_skills: Set[str]
    missing_skills: Set[str]
    extra_skills: Set[str]
    similarity_score: float

@dataclass
class AnalysisReport:
    """Data class for complete analysis report."""
    resume_extraction: ExtractionResult
    jd_extraction: ExtractionResult
    match_result: MatchResult
    resume_insights: Optional[str] = None
    jd_insights: Optional[str] = None

class SessionKeys:
    """Constants for Streamlit session state keys."""
    UPLOADED_FILE = "uploaded_file"
    RESUME_TEXT = "resume_text"
    JD_TEXT = "jd_text"
    
    # AI Extraction Results
    GENAI_RESUME_SKILLS = "genai_resume_skill_json"
    GENAI_JD_SKILLS = "jd_skill_json"
    GENAI_RESUME_TIME = "genai_resume_time"
    GENAI_JD_TIME = "genai_jd_time"
    
    # NLP Extraction Results
    NLP_RESUME_SKILLS = "nlp_resume_skills"
    NLP_JD_SKILLS = "nlp_jd_skills"
    NLP_RESUME_TIME = "nlp_resume_time"
    NLP_JD_TIME = "nlp_jd_time"
