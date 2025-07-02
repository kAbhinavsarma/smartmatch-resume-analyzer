"""
Helper utilities and miscellaneous functions.
"""
import re
import tiktoken
from typing import Set, Tuple
from config.settings import COST_CONFIG

class AnalysisHelpers:
    """Collection of helper functions for analysis operations."""
    
    @staticmethod
    def estimate_gpt4o_cost(input_text: str, output_text: str, 
                          input_rate: float = None, output_rate: float = None) -> Tuple[str, int, int]:
        """
        Estimate the cost of GPT-4 API usage.
        
        Args:
            input_text: Input text sent to GPT
            output_text: Output text received from GPT
            input_rate: Cost per 1K input tokens (optional)
            output_rate: Cost per 1K output tokens (optional)
            
        Returns:
            Tuple of (formatted_cost, input_tokens, output_tokens)
        """
        input_rate = input_rate or COST_CONFIG["gpt4o_input_rate"]
        output_rate = output_rate or COST_CONFIG["gpt4o_output_rate"]
        
        enc = tiktoken.encoding_for_model("gpt-4o")
        input_tokens = len(enc.encode(input_text))
        output_tokens = len(enc.encode(output_text))
        
        input_cost = (input_tokens / 1000) * input_rate
        output_cost = (output_tokens / 1000) * output_rate
        total_cost = input_cost + output_cost
        
        return f"${total_cost:.4f}", input_tokens, output_tokens
    
    @staticmethod
    def estimate_gpt4o_processing_cost(input_text: str, output_text: str, 
                                     input_rate: float = None, output_rate: float = None) -> Tuple[str, int, int]:
        """
        Estimate the cost of GPT-4 processing with professional analysis.
        
        Args:
            input_text: Input text sent to GPT
            output_text: Output text received from GPT
            input_rate: Cost per 1K input tokens (optional)
            output_rate: Cost per 1K output tokens (optional)
            
        Returns:
            Tuple of (formatted_cost, input_tokens, output_tokens)
        """
        return AnalysisHelpers.estimate_gpt4o_cost(input_text, output_text, input_rate, output_rate)

def generate_analysis_report(score: float, matched: Set[str], missing: Set[str]) -> bytes:
    """
    Generate a comprehensive analysis report in CSV format.
    
    This function creates a detailed analysis report containing skill matching
    results, similarity scores, and professional recommendations.
    
    Args:
        score: Overall similarity score between resume and job description
        matched: Set of skills that were successfully matched
        missing: Set of skills that are missing from the resume
        
    Returns:
        CSV report data as bytes
    """
    from src.utils.report_generator import report_generator
    return report_generator.export_csv_report(score, matched, missing)

# Create alias for the main class to match import expectations
AnalysisUtilities = AnalysisHelpers
