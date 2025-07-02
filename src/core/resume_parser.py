"""
Resume Parser Module

Handles parsing and categorization of resume content into structured sections.
Provides clean, categorized content extraction from raw PDF text.

Author: SmartMatch Development Team
"""

import re
from typing import Dict, List, Tuple, Set


class ResumeParser:
    """Professional resume parser with advanced section detection and categorization."""
    
    def __init__(self):
        """Initialize the resume parser with predefined patterns and headers."""
        self.section_headers = {
            'contact', 'professional summary', 'summary', 'objective',
            'skills', 'technical skills', 'core competencies', 'technologies',
            'experience', 'work experience', 'professional experience', 'employment',
            'education', 'academic background', 'qualifications',
            'projects', 'certifications', 'achievements', 'awards'
        }
        
        self._initialize_patterns()
    
    def _initialize_patterns(self) -> None:
        """Initialize regex patterns for content categorization."""
        self.name_patterns = [
            r'^[A-Z][a-z]+ [A-Z][a-z]+$',  # First Last
            r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$',  # First M. Last
            r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$',  # First Middle Last
        ]
        
        self.contact_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',  # Phone
            r'linkedin\.com/in/[\w-]+',  # LinkedIn
            r'github\.com/[\w-]+',  # GitHub
            r'\b(?:email|phone|tel|mobile|cell|linkedin|github):\s*',  # Contact labels
        ]
        
        self.experience_patterns = [
            r'\b(?:data scientist|software engineer|analyst|developer|manager|consultant|specialist|coordinator|director)\b',
            r'\b(?:company|corp|corporation|inc|ltd|llc|university|institute)\b',
            r'\b(?:built|developed|managed|led|created|designed|implemented|analyzed|collaborated|automated)\b',
            r'\d{4}\s*[-\-]\s*(?:\d{4}|present|current)',  # Date ranges
            r'\b(?:years?|months?)\s+(?:of\s+)?(?:experience|work)',
        ]
        
        self.education_patterns = [
            r'\b(?:university|college|school|institute|academy)\b',
            r'\b(?:bachelor|master|phd|doctorate|degree|diploma|certificate)\b',
            r'\b(?:b\.s|b\.a|m\.s|m\.a|ph\.d|bs|ba|ms|ma)\b',
            r'\b(?:computer science|engineering|mathematics|business|mba)\b',
        ]
        
        self.skills_patterns = [
            r'\b(?:python|java|javascript|sql|html|css|react|angular|node|django|flask)\b',
            r'\b(?:machine learning|data science|artificial intelligence|deep learning|nlp)\b',
            r'\b(?:pandas|numpy|scikit-learn|tensorflow|pytorch|matplotlib|seaborn)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|git|jenkins)\b',
            r'\b(?:excel|powerbi|tableau|stata|r|matlab|sas|spss)\b',
        ]
    
    def _clean_text(self, text: str) -> List[str]:
        """Clean and normalize resume text into processable lines."""
        # Normalize text format
        text = text.replace('|', '\n')
        text = re.sub(r'[•·▪▫◦‣⁃]', '•', text)  # Normalize bullet points
        text = re.sub(r' {3,}', '\n', text)  # Convert multiple spaces to line breaks
        
        # Extract valid lines
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line and len(line) > 1:
                lines.append(line)
        
        return lines
    
    def _categorize_line(self, line: str, line_index: int) -> Tuple[str, bool]:
        """Categorize a single line of resume content."""
        line_lower = line.lower().strip()
        
        # Skip section headers
        if line_lower in self.section_headers or len(line.strip()) < 3:
            return '', False
            
        # Skip standalone section headers with minimal formatting
        if (len(line) < 30 and 
            any(header in line_lower for header in self.section_headers) and
            not any(re.search(pattern, line_lower) for pattern in 
                   self.name_patterns + self.contact_patterns + self.experience_patterns + 
                   self.education_patterns + self.skills_patterns)):
            return '', False
        
        # Skip lines that are just bullet points or dashes
        if re.match(r'^[•\-–—\*\+\s]*$', line):
            return '', False
        
        # Categorize meaningful content
        # Check for name (usually first few lines)
        if (line_index < 3 and 
            any(re.match(pattern, line.strip()) for pattern in self.name_patterns) and
            not any(re.search(pattern, line_lower) for pattern in 
                   self.contact_patterns + self.experience_patterns + 
                   self.education_patterns + self.skills_patterns)):
            return 'contact', True
        
        # Contact information
        elif any(re.search(pattern, line_lower) for pattern in self.contact_patterns):
            return 'contact', True
        
        # Experience content
        elif any(re.search(pattern, line_lower) for pattern in self.experience_patterns):
            return 'experience', True
        
        # Education content
        elif any(re.search(pattern, line_lower) for pattern in self.education_patterns):
            return 'education', True
        
        # Skills content (but not just the word "skills")
        elif (any(re.search(pattern, line_lower) for pattern in self.skills_patterns) and 
              line_lower not in ['skills', 'technical skills', 'core skills']):
            return 'skills', True
        
        # Everything else (excluding obvious headers)
        elif len(line.strip()) > 10:
            return 'other', True
        
        return '', False
    
    def _clean_sections(self, sections: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Clean up sections by removing any remaining headers and limiting size."""
        # Clean up any remaining section headers
        for section_key in ['contact', 'experience', 'education', 'skills', 'other']:
            sections[section_key] = [
                item for item in sections[section_key] 
                if len(item.strip()) > 10 and item.lower().strip() not in self.section_headers
            ]
        
        # Clean up ordered content
        sections['ordered_content'] = [
            (category, item) for category, item in sections['ordered_content']
            if len(item.strip()) > 10 and item.lower().strip() not in self.section_headers
        ]
        
        # Limit sections to reasonable sizes
        for key in sections:
            if key != 'ordered_content' and len(sections[key]) > 15:
                sections[key] = sections[key][:15]
        
        return sections
    
    def parse_resume_sections(self, text: str) -> Dict[str, List]:
        """
        Parse resume text into structured sections.
        
        Args:
            text: Raw extracted text from resume
            
        Returns:
            Dictionary containing clean, ordered content without section headers
        """
        # Initialize sections
        sections = {
            'contact': [],
            'experience': [],
            'education': [],
            'skills': [],
            'other': [],
            'ordered_content': []
        }
        
        # Clean and process text
        lines = self._clean_text(text)
        
        # Process each line
        for i, line in enumerate(lines):
            category, is_valid = self._categorize_line(line, i)
            
            if is_valid and category:
                sections[category].append(line)
                sections['ordered_content'].append((category, line))
        
        # Clean and finalize sections
        return self._clean_sections(sections)
