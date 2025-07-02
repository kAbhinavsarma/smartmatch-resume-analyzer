"""
Semantic skill matching using sentence transformers and similarity algorithms.
"""
from sentence_transformers import SentenceTransformer, util
from typing import Set, Tuple
from config.settings import AI_CONFIG

class SkillMatcher:
    """Handles semantic skill matching between resume and job description skills."""
    
    def __init__(self, model_name: str = None, threshold: float = None):
        """
        Initialize the skill matcher.
        
        Args:
            model_name: Name of the sentence transformer model
            threshold: Similarity threshold for matching
        """
        self.model_name = model_name or AI_CONFIG["sentence_transformer_model"]
        self.threshold = threshold or AI_CONFIG["semantic_matching_threshold"]
        self.model = SentenceTransformer(self.model_name)
    
    def semantic_skill_match(self, resume_skills: Set[str], jd_skills: Set[str]) -> Tuple[Set[str], Set[str]]:
        """
        Match skills using semantic similarity (embeddings).
        
        Args:
            resume_skills: Set of skills from resume
            jd_skills: Set of skills from job description
            
        Returns:
            Tuple of (matched_skills, missing_skills)
        """
        matches = set()
        missing = set(jd_skills)
        
        if not resume_skills or not jd_skills:
            return matches, missing
        
        resume_skills_list = list(resume_skills)
        jd_skills_list = list(jd_skills)
        
        # Encode skills to vectors
        resume_vecs = self.model.encode(resume_skills_list, convert_to_tensor=True)
        jd_vecs = self.model.encode(jd_skills_list, convert_to_tensor=True)
        
        # Find matches above threshold
        for i, jd_skill in enumerate(jd_skills_list):
            sims = util.cos_sim(jd_vecs[i], resume_vecs)[0]
            max_sim = sims.max().item()
            if max_sim >= self.threshold:
                matches.add(jd_skill)
                missing.discard(jd_skill)
        
        return matches, missing
    
    def compute_similarity_sbert(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
        
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        return float(util.cos_sim(emb1, emb2)[0][0])

# Global instance for backward compatibility
skill_matcher = SkillMatcher()

def perform_semantic_skill_matching(resume_skills: Set[str], jd_skills: Set[str]) -> Tuple[Set[str], Set[str]]:
    """
    Perform semantic skill matching between resume and job description skills.
    
    This function provides professional-grade skill matching using advanced
    semantic similarity algorithms and sentence transformers.
    
    Args:
        resume_skills: Set of skills extracted from resume
        jd_skills: Set of skills from job description
        
    Returns:
        Tuple of (matched_skills, missing_skills)
    """
    return skill_matcher.semantic_skill_match(resume_skills, jd_skills)

def calculate_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity score between two text segments.
    
    This function computes the semantic similarity using sentence transformers
    and cosine similarity for professional text analysis.
    
    Args:
        text1: First text segment for comparison
        text2: Second text segment for comparison
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    return skill_matcher.compute_similarity_sbert(text1, text2)
