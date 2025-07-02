"""
NLP processing module using spaCy for skill extraction and analysis.
"""
import re
import spacy
from spacy.matcher import PhraseMatcher
from typing import Set
from data.skill_categories import PROFESSIONAL_SKILL_CATEGORIES, get_all_professional_skills

class NLPProcessor:
    """Handles NLP-based skill extraction using spaCy."""
    
    def __init__(self, model_name: str = "en_core_web_md"):
        """
        Initialize the NLP processor.
        
        Args:
            model_name: Name of the spaCy model to use
        """
        self.model_name = model_name
        self.nlp = spacy.load(model_name)
        self.all_skills = get_all_professional_skills()
    
    def clean_jd_text(self, jd_text: str) -> str:
        """
        Clean and normalize job description text.
        
        Args:
            jd_text: Raw job description text
            
        Returns:
            Cleaned and normalized text
        """
        jd_text = jd_text.lower()
        jd_text = re.sub(r"[^a-z0-9\s]", " ", jd_text)
        jd_text = re.sub(r"\s+", " ", jd_text)
        return jd_text.strip()
    
    def extract_skills_spacy(self, text: str) -> Set[str]:
        """
        Extract skills from text using spaCy NER and PhraseMatcher.
        
        Args:
            text: Input text to extract skills from
            
        Returns:
            Set of found skills
        """
        found_skills = set()
        
        # spaCy NER-based extraction
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"SKILL", "ORG", "PRODUCT"}:
                ent_text = ent.text.lower()
                if ent_text in [s.lower() for s in self.all_skills]:
                    found_skills.add(ent_text)
        
        # PhraseMatcher for robust multi-word skill detection
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in self.all_skills]
        matcher.add("SKILLS", patterns)
        matches = matcher(doc)
        
        for match_id, start, end in matches:
            found_skills.add(doc[start:end].text.lower())
        
        return found_skills

# Global instance for backward compatibility
nlp_processor = NLPProcessor()

def extract_skills_using_nlp(text: str) -> Set[str]:
    """
    Extract skills from text using advanced NLP processing.
    
    This function provides professional-grade skill extraction using spaCy's
    named entity recognition and phrase matching capabilities.
    
    Args:
        text: Input text to extract skills from
        
    Returns:
        Set of found skills
    """
    return nlp_processor.extract_skills_spacy(text)
