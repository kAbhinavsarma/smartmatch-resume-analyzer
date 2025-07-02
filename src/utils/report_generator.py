"""
Professional Report Generation for Resume Analysis

This module provides enterprise-grade report generation capabilities for resume
and job description analysis results. Supports PDF and CSV export formats with
professional styling and comprehensive data presentation.

Classes:
    ReportGenerator: Main class for generating formatted analysis reports

Functions:
    create_pdf_analysis_report: Generate PDF reports from HTML content
    generate_html_report: Create professional HTML reports
    export_csv_report: Export analysis data to CSV format

Author: Resume Analysis Team
Version: 1.0.0
"""
from xhtml2pdf import pisa
import tempfile
from io import StringIO
from typing import Set, Optional, Dict, Any
import json
import logging

# Configure logging for production monitoring
logger = logging.getLogger(__name__)

class ProfessionalReportGenerator:
    """
    Enterprise-grade report generation for resume analysis results.
    
    Provides comprehensive reporting capabilities with professional formatting
    for recruitment workflows and candidate assessment documentation.
    """
    
    def create_pdf_analysis_report(self, html_content: str) -> str:
        """
        Convert HTML content to professional PDF report.
        
        Args:
            html_content: Well-formatted HTML content for conversion
            
        Returns:
            Absolute path to the generated PDF file
            
        Raises:
            Exception: If PDF generation fails
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                pdf_status = pisa.CreatePDF(html_content, dest=temp_pdf)
                
                if pdf_status.err:
                    logger.error(f"PDF generation encountered errors: {pdf_status.err}")
                    raise Exception("PDF generation failed")
                
                logger.info(f"PDF report generated successfully: {temp_pdf.name}")
                return temp_pdf.name
                
        except Exception as e:
            logger.error(f"Error creating PDF report: {e}")
            raise
    def generate_html_report(self, resume_identifier: str, job_summary: str, match_score: float, 
                           matched_skills: Set[str], missing_skills: Set[str], 
                           job_analysis: Optional[str] = None, 
                           candidate_summary: Optional[str] = None) -> str:
        """
        Generate professional HTML report for analysis results.
        
        Args:
            resume_identifier: Candidate name or resume identifier
            job_summary: Brief job description summary
            match_score: Calculated match score (0.0 to 1.0)
            matched_skills: Set of skills found in both resume and job description
            missing_skills: Set of skills required but not found in resume
            job_analysis: Optional AI-generated job requirements analysis
            candidate_summary: Optional AI-generated candidate profile summary
            
        Returns:
            Professional HTML report string suitable for PDF conversion or web display
        """
        # Convert score to percentage for display
        score_percentage = match_score * 100
        
        # Determine score color based on performance thresholds
        if score_percentage >= 80:
            score_color = "#2e7d32"  # Strong green
        elif score_percentage >= 60:
            score_color = "#f57c00"  # Amber
        else:
            score_color = "#d32f2f"  # Red
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume Analysis Report - {resume_identifier}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f8f9fa;
                    color: #212529;
                    margin: 0;
                    padding: 20px;
                    line-height: 1.6;
                }}
                .report-container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: #ffffff;
                    padding: 18px 18px 22px 18px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.08);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 18px;
                    border-bottom: 2px solid #0066cc;
                    padding-bottom: 10px;
                }}
                .report-title {{
                    color: #0066cc;
                    font-size: 1.5em;
                    font-weight: 600;
                    margin-bottom: 6px;
                }}
                .report-subtitle {{
                    color: #6c757d;
                    font-size: 1em;
                    margin: 0;
                }}
                .match-score {{
                    font-size: 1.5em;
                    font-weight: bold;
                    color: {score_color};
                    text-align: center;
                    margin: 16px 0 12px 0;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    border: 2px solid {score_color};
                }}
                .section {{
                    margin-bottom: 18px;
                }}
                .section-title {{
                    color: #0066cc;
                    font-size: 1.1em;
                    font-weight: 600;
                    margin-bottom: 8px;
                    display: flex;
                    align-items: center;
                }}
                .skill-count {{
                    background: #0066cc;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8em;
                    margin-left: 10px;
                    font-weight: 500;
                }}
                .missing-count {{
                    background: #dc3545;
                }}
                .skills-grid {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 12px;
                    margin-top: 15px;
                    line-height: 1.8;
                }}
                .skill-tag {{
                    background: #e3f2fd;
                    color: #1565c0;
                    padding: 8px 14px;
                    border-radius: 16px;
                    font-size: 0.9em;
                    font-weight: 500;
                    border: 1px solid #bbdefb;
                    margin: 2px;
                    display: inline-block;
                    white-space: nowrap;
                }}
                .missing-skill-tag {{
                    background: #ffebee;
                    color: #c62828;
                    border: 1px solid #ffcdd2;
                }}
                .analysis-box {{
                    background: #f8f9fa;
                    border-left: 4px solid #0066cc;
                    padding: 20px;
                    margin-top: 15px;
                    border-radius: 0 6px 6px 0;
                    font-style: italic;
                    color: #495057;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #dee2e6;
                    color: #6c757d;
                    font-size: 0.9em;
                }}
                @media print {{
                    body {{ padding: 0; }}
                    .report-container {{ box-shadow: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="report-container">
                <div class="header">
                    <h1 class="report-title">Professional Resume Analysis Report</h1>
                    <p class="report-subtitle">Comprehensive Skill Matching and Gap Analysis</p>
                </div>
                
                <div class="match-score">
                    Overall Match Score: {score_percentage:.1f}%
                </div>"""
        
        # Add job analysis section if provided
        if job_analysis:
            html_content += f"""
                <div class="section">
                    <h2 class="section-title">Job Requirements Analysis</h2>
                    <div class="analysis-box">{job_analysis}</div>
                </div>"""
        
        # Add candidate summary section if provided
        if candidate_summary:
            html_content += f"""
                <div class="section">
                    <h2 class="section-title">Candidate Profile Summary</h2>
                    <div class="analysis-box">{candidate_summary}</div>
                </div>"""
        
        # Add matched skills section
        html_content += f"""
                <div class="section">
                    <h2 class="section-title">
                        Skills Match
                        <span class="skill-count">{len(matched_skills)} Skills</span>
                    </h2>
                    <div class="skills-grid">"""
        
        for skill in sorted(matched_skills):
            html_content += f'<span class="skill-tag">{skill.title()}</span> '
        
        html_content += """
                    </div>
                </div>"""
        
        # Add missing skills section
        html_content += f"""
                <div class="section">
                    <h2 class="section-title">
                        Skills Gap
                        <span class="skill-count missing-count">{len(missing_skills)} Skills</span>
                    </h2>
                    <div class="skills-grid">"""
        
        for skill in sorted(missing_skills):
            html_content += f'<span class="skill-tag missing-skill-tag">{skill.title()}</span> '
        
        html_content += f"""
                    </div>
                </div>
                
                <div class="footer">
                    <p>Generated by SmartMatch Resume Analyzer | Professional Recruitment Tools</p>
                </div>
            </div>
        </body>
        </html>"""
        
        return html_content
    def export_csv_analysis_report(self, match_score: float, matched_skills: Set[str], 
                                 missing_skills: Set[str], filename: str = "analysis_report.csv") -> bytes:
        """
        Export comprehensive analysis results to CSV format.
        
        Args:
            match_score: Calculated match score (0.0 to 1.0)
            matched_skills: Set of skills found in both resume and job description  
            missing_skills: Set of skills required but not found in resume
            filename: Output filename for the CSV report
            
        Returns:
            CSV content as UTF-8 encoded bytes suitable for download
        """
        try:
            output = StringIO()
            
            # Report header and metadata
            output.write("SmartMatch Resume Analysis Report\n")
            output.write("Professional Skill Matching and Gap Analysis\n")
            output.write("\n")
            
            # Overall metrics
            output.write("ANALYSIS SUMMARY\n")
            # Handle None similarity score gracefully
            score_display = f"{(match_score or 0.0)*100:.2f}%" 
            output.write(f"Overall Match Score,{score_display}\n")
            output.write(f"Skills Matched,{len(matched_skills)}\n")
            output.write(f"Skills Missing,{len(missing_skills)}\n")
            output.write(f"Total Skills Evaluated,{len(matched_skills) + len(missing_skills)}\n")
            output.write("\n")
            
            # Matched skills section
            output.write("SKILLS SUCCESSFULLY MATCHED\n")
            output.write("Skill Name,Category\n")
            for skill in sorted(matched_skills):
                # You could enhance this to include skill categories if available
                output.write(f"{skill.title()},Technical\n")
            output.write("\n")
            
            # Missing skills section
            output.write("SKILLS REQUIRING DEVELOPMENT\n")
            output.write("Skill Name,Priority,Category\n")
            for skill in sorted(missing_skills):
                # You could enhance this to include priority levels if available
                output.write(f"{skill.title()},High,Technical\n")
            
            logger.info(f"CSV report generated successfully: {filename}")
            return output.getvalue().encode("utf-8")
            
        except Exception as e:
            logger.error(f"Error generating CSV report: {e}")
            raise

    def export_csv_report(self, score: float, matched: Set[str], missing: Set[str], 
                         filename: str = "analysis_report.csv") -> bytes:
        """
        Export analysis results to CSV format (alias for export_csv_analysis_report).
        
        Args:
            score: Overall similarity score (0.0 to 1.0)
            matched: Set of successfully matched skills
            missing: Set of skills missing from resume
            filename: Target filename for the CSV report
            
        Returns:
            CSV content as UTF-8 encoded bytes suitable for download
        """
        return self.export_csv_analysis_report(score, matched, missing, filename)

# Global instance for enterprise use and backward compatibility
professional_report_generator = ProfessionalReportGenerator()

# Legacy compatibility functions
def create_pdf_analysis_report(html_content: str) -> str:
    """
    Legacy function for backward compatibility.
    Use professional_report_generator.create_pdf_analysis_report instead.
    """
    return professional_report_generator.create_pdf_analysis_report(html_content)

def generate_html_report(resume_name: str, jd_summary: str, score: float, 
                        matched: Set[str], missing: Set[str], 
                        job_insights: Optional[str] = None, 
                        resume_insights: Optional[str] = None) -> str:
    """
    Legacy function for backward compatibility.
    Use professional_report_generator.generate_html_report instead.
    """
    return professional_report_generator.generate_html_report(
        resume_identifier=resume_name, 
        job_summary=jd_summary, 
        match_score=score, 
        matched_skills=matched, 
        missing_skills=missing, 
        job_analysis=job_insights, 
        candidate_summary=resume_insights
    )

def export_csv_report(score: float, matched: Set[str], missing: Set[str], 
                     filename: str = "analysis_report.csv") -> bytes:
    """
    Legacy function for backward compatibility.
    Use professional_report_generator.export_csv_analysis_report instead.
    """
    return professional_report_generator.export_csv_analysis_report(
        match_score=score, 
        matched_skills=matched, 
        missing_skills=missing, 
        filename=filename
    )

# Global instance for production use
report_generator = professional_report_generator
