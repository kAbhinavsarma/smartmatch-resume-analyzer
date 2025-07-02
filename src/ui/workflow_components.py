"""
UI Workflow Components

Modular workflow components for the SmartMatch application.
Handles the main UI workflow steps with clear separation of concerns.

Author: SmartMatch Development Team
"""

import streamlit as st
import time
import re
from typing import Dict, Set, Any, Optional, Tuple
import plotly.express as px

from src.core.text_extractor import extract_text_from_pdf_document
from src.core.nlp_processor import extract_skills_using_nlp
from src.core.skill_matcher import perform_semantic_skill_matching, calculate_similarity_score
from src.ai.gpt_handlers import (
    extract_job_description_skills,
    extract_resume_skills,
    generate_skill_summary,
    analyze_job_requirements,
    recommend_skill_improvement,
    get_single_skill_recommendation
)
from src.ui.components import ProfessionalUIComponents
from src.utils.helpers import AnalysisUtilities, generate_analysis_report
from src.utils.report_generator import create_pdf_analysis_report, generate_html_report
from src.core.resume_parser import ResumeParser
from data.skill_categories import PROFESSIONAL_SKILL_RECOMMENDATIONS
from src.ui.styles import (
    get_metric_card_styles,
    get_radio_button_styles,
    get_expandable_content_styles,
    get_download_button_styles
)


class WorkflowComponents:
    """Manages the main workflow components for the SmartMatch application."""
    
    def __init__(self):
        """Initialize workflow components."""
        self.resume_parser = ResumeParser()
    
    def render_resume_upload_section(self) -> None:
        """Render the resume upload and processing section."""
        ProfessionalUIComponents.render_analysis_section_header("Resume Upload")
        st.markdown(
            "<div style='font-size:1.1rem; margin-bottom: 1em;'>"
            "Upload resume document as PDF for comprehensive skill analysis."
            "</div>",
            unsafe_allow_html=True,
        )

        # File upload widget
        uploaded_resume_file = st.file_uploader("Select resume document (PDF format only)", type="pdf")
        if uploaded_resume_file:
            st.session_state["uploaded_resume_file"] = uploaded_resume_file
            extracted_resume_text = extract_text_from_pdf_document(uploaded_resume_file)
            st.session_state["extracted_resume_text"] = extracted_resume_text

        # Process uploaded resume
        extracted_resume_text = st.session_state.get("extracted_resume_text", "")
        if extracted_resume_text:
            st.success("Resume uploaded and processed successfully!")
            self._render_resume_preview(extracted_resume_text)
            st.markdown("---")
            self._render_skill_analysis_columns(extracted_resume_text)
    
    def _render_resume_preview(self, extracted_resume_text: str) -> None:
        """Render the resume preview section."""
        with st.expander("Preview Extracted Text"):
            parsed_sections = self.resume_parser.parse_resume_sections(extracted_resume_text)
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 25px; border-radius: 12px; border-left: 4px solid #1976d2; 
                        max-height: 500px; overflow-y: auto; font-family: "Segoe UI", sans-serif;'>
                <h4 style='color: #1976d2; margin-top: 0; margin-bottom: 20px;'>
                    Document Content Preview
                </h4>
            """, unsafe_allow_html=True)
            
            self._render_ordered_content(parsed_sections)
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    def _render_ordered_content(self, parsed_sections: Dict) -> None:
        """Render ordered resume content."""
        ordered_content = parsed_sections.get('ordered_content', [])
        
        if ordered_content:
            for category, item in ordered_content:
                clean_item = item.strip()
                if len(clean_item) < 10:
                    continue
                    
                # Add bullet point if not already present
                if not clean_item.startswith('•') and not clean_item.startswith('-'):
                    clean_item = f"• {clean_item}"
                elif clean_item.startswith('-'):
                    clean_item = clean_item.replace('-', '•', 1)
                
                st.markdown(f"""
                <div style='background: white; padding: 8px 15px; margin: 5px 0; 
                            border-radius: 6px; border-left: 3px solid #1976d2; 
                            font-size: 0.9rem; line-height: 1.5; color: #333;'>
                    {clean_item}
                </div>
                """, unsafe_allow_html=True)
        else:
            self._render_fallback_content(parsed_sections)
    
    def _render_fallback_content(self, parsed_sections: Dict) -> None:
        """Render fallback content when ordered content is unavailable."""
        all_content = []
        for section_name in ['contact', 'experience', 'education', 'skills', 'other']:
            section_content = parsed_sections.get(section_name, [])
            all_content.extend(section_content)
            
        for item in all_content:
            clean_item = item.strip()
            if len(clean_item) > 10:
                if not clean_item.startswith('•'):
                    clean_item = f"• {clean_item}"
                st.markdown(f"""
                <div style='background: white; padding: 8px 15px; margin: 5px 0; 
                            border-radius: 6px; border-left: 3px solid #1976d2; 
                            font-size: 0.9rem; line-height: 1.5; color: #333;'>
                    {clean_item}
                </div>
                """, unsafe_allow_html=True)
    
    def _render_skill_analysis_columns(self, extracted_resume_text: str) -> None:
        """Render the dual column skill analysis section."""
        ai_analysis_column, nlp_analysis_column = st.columns(2)
        
        with ai_analysis_column:
            self._render_ai_analysis_column(extracted_resume_text)
        
        with nlp_analysis_column:
            self._render_nlp_analysis_column(extracted_resume_text)
        
        # Show comparison if both completed
        if (st.session_state.get("ai_extracted_resume_skills") and 
            st.session_state.get("nlp_extracted_resume_skills")):
            self._render_analysis_comparison(extracted_resume_text)
    
    def _render_ai_analysis_column(self, extracted_resume_text: str) -> None:
        """Render AI-powered skill analysis column."""
        ProfessionalUIComponents.render_professional_gradient_box(
            "<b>AI-Powered Skill Analysis</b>", "#e3f2fd", "#f1f8e9", 90
        )
        
        ai_button_disabled = st.session_state.get("ai_processing", False)
        ai_button_clicked = st.button("Analyze with AI", key="analyze_resume_with_ai", disabled=ai_button_disabled)
        
        if ai_button_clicked:
            st.session_state["ai_processing"] = True
            st.rerun()
            
        if st.session_state.get("ai_processing", False):
            analysis_start_time = time.time()
            with st.spinner("Analyzing resume content..."):
                st.session_state["ai_extracted_resume_skills"] = extract_resume_skills(extracted_resume_text)
            st.session_state["ai_resume_analysis_time"] = time.time() - analysis_start_time
            st.session_state["ai_processing"] = False
            
        ai_extracted_resume_skills = st.session_state.get("ai_extracted_resume_skills", {})
        if ai_extracted_resume_skills:
            self._display_ai_skills_table(ai_extracted_resume_skills, extracted_resume_text)
    
    def _render_nlp_analysis_column(self, extracted_resume_text: str) -> None:
        """Render NLP skill analysis column."""
        ProfessionalUIComponents.render_professional_gradient_box(
            "<b>Traditional NLP Analysis</b>", "#e8f5e8", "#f1f8e9", 90
        )
        
        nlp_button_disabled = st.session_state.get("nlp_processing", False)
        nlp_button_clicked = st.button("Analyze with NLP", key="analyze_resume_with_nlp", disabled=nlp_button_disabled)
        
        if nlp_button_clicked:
            st.session_state["nlp_processing"] = True
            st.rerun()
            
        if st.session_state.get("nlp_processing", False):
            analysis_start_time = time.time()
            with st.spinner("Processing resume with NLP..."):
                st.session_state["nlp_extracted_resume_skills"] = extract_skills_using_nlp(extracted_resume_text)
            st.session_state["nlp_resume_analysis_time"] = time.time() - analysis_start_time
            st.session_state["nlp_processing"] = False
            
        nlp_extracted_resume_skills = st.session_state.get("nlp_extracted_resume_skills", set())
        if nlp_extracted_resume_skills:
            self._display_nlp_skills_table(nlp_extracted_resume_skills)
    
    def _display_ai_skills_table(self, ai_extracted_resume_skills: Dict, extracted_resume_text: str) -> None:
        """Display AI-extracted skills in a professional table."""
        st.markdown("<b>AI-Extracted Skills</b>", unsafe_allow_html=True)
        skill_headers = ["Skill", "Category", "Proficiency Level"]
        skill_rows = [
            [skill_name, skill_props.get("category", "General"), skill_props.get("proficiency", "Intermediate")]
            for skill_name, skill_props in ai_extracted_resume_skills.items()
        ]
        skills_table_html = ProfessionalUIComponents.create_professional_html_table(skill_headers, skill_rows)
        st.markdown(skills_table_html, unsafe_allow_html=True)
        
        with st.expander("Detailed AI Analysis"):
            if "cached_resume_analysis" not in st.session_state:
                st.session_state["cached_resume_analysis"] = generate_skill_summary(
                    extracted_resume_text, ai_extracted_resume_skills
                )
            st.info(st.session_state["cached_resume_analysis"])
    
    def _display_nlp_skills_table(self, nlp_extracted_resume_skills: Set) -> None:
        """Display NLP-extracted skills in a professional table."""
        st.markdown("<b>NLP-Extracted Skills</b>", unsafe_allow_html=True)
        skill_headers = ["Skill", "Detected Context"]
        skill_rows = [[skill_name, "Resume Context"] for skill_name in sorted(nlp_extracted_resume_skills)]
        skills_table_html = ProfessionalUIComponents.create_professional_html_table(skill_headers, skill_rows)
        st.markdown(skills_table_html, unsafe_allow_html=True)
    
    def _render_analysis_comparison(self, extracted_resume_text: str) -> None:
        """Render skill extraction comparison table."""
        ai_input_sample = extracted_resume_text[:2000]
        ai_output_sample = str(st.session_state["ai_extracted_resume_skills"])
        estimated_cost, input_tokens, output_tokens = AnalysisUtilities.estimate_gpt4o_processing_cost(
            ai_input_sample, ai_output_sample
        )
        
        st.markdown("---")
        ProfessionalUIComponents.render_analysis_section_header("Analysis Comparison", "Skill Extraction Comparison")
        ProfessionalUIComponents.render_professional_extraction_comparison_table(
            len(st.session_state['ai_extracted_resume_skills']),
            st.session_state.get('ai_resume_analysis_time', 0),
            len(st.session_state['nlp_extracted_resume_skills']),
            st.session_state.get('nlp_resume_analysis_time', 0),
            estimated_cost
        )
    
    def render_job_description_section(self) -> None:
        """Render the job description analysis section."""
        ProfessionalUIComponents.render_analysis_section_header("Job Description Analysis")
        st.markdown(
            "<div style='font-size:1.1rem; margin-bottom: 1em;'>"
            "Paste the job description below to analyze required skills and qualifications."
            "</div>",
            unsafe_allow_html=True,
        )

        job_description_text = st.text_area("Paste the complete job description here", height=200)
        st.markdown("---")
        
        self._render_job_analysis_columns(job_description_text)
    
    def _render_job_analysis_columns(self, job_description_text: str) -> None:
        """Render dual column job analysis section."""
        ai_jd_column, nlp_jd_column = st.columns(2)
        
        with ai_jd_column:
            self._render_ai_job_analysis(job_description_text)
        
        with nlp_jd_column:
            self._render_nlp_job_analysis(job_description_text)
        
        # Show comparison if both completed
        if (st.session_state.get("ai_extracted_job_skills") and 
            st.session_state.get("nlp_extracted_job_skills")):
            self._render_job_analysis_comparison(job_description_text)
    
    def _render_ai_job_analysis(self, job_description_text: str) -> None:
        """Render AI-powered job description analysis."""
        ProfessionalUIComponents.render_professional_gradient_box(
            "<b>AI-Powered Job Analysis</b>", "#e3f2fd", "#f1f8e9", 90
        )
        
        ai_jd_button_disabled = st.session_state.get("ai_jd_processing", False)
        ai_jd_button_clicked = st.button("Analyze with AI", key="analyze_job_description_with_ai", disabled=ai_jd_button_disabled)
        
        if ai_jd_button_clicked:
            st.session_state["ai_jd_processing"] = True
            st.rerun()
            
        if st.session_state.get("ai_jd_processing", False):
            analysis_start_time = time.time()
            if job_description_text.strip():
                st.session_state["job_description_text"] = job_description_text
                with st.spinner("Analyzing job requirements..."):
                    st.session_state["ai_extracted_job_skills"] = extract_job_description_skills(job_description_text)
                st.session_state["ai_job_analysis_time"] = time.time() - analysis_start_time
            st.session_state["ai_jd_processing"] = False
                
        ai_extracted_job_skills = st.session_state.get("ai_extracted_job_skills", {})
        if ai_extracted_job_skills:
            self._display_ai_job_skills(ai_extracted_job_skills, job_description_text)
    
    def _render_nlp_job_analysis(self, job_description_text: str) -> None:
        """Render NLP job description analysis."""
        ProfessionalUIComponents.render_professional_gradient_box(
            "<b>Traditional NLP Analysis</b>", "#e3f2fd", "#f1f8e9", 90
        )
        
        nlp_jd_button_disabled = st.session_state.get("nlp_jd_processing", False)
        nlp_jd_button_clicked = st.button("Analyze with NLP", key="analyze_job_description_with_nlp", disabled=nlp_jd_button_disabled)
        
        if nlp_jd_button_clicked:
            st.session_state["nlp_jd_processing"] = True
            st.rerun()
            
        if st.session_state.get("nlp_jd_processing", False):
            analysis_start_time = time.time()
            if job_description_text.strip():
                st.session_state["job_description_text"] = job_description_text
                with st.spinner("Processing job requirements with NLP..."):
                    st.session_state["nlp_extracted_job_skills"] = extract_skills_using_nlp(job_description_text)
                st.session_state["nlp_job_analysis_time"] = time.time() - analysis_start_time
            st.session_state["nlp_jd_processing"] = False
                
        nlp_extracted_job_skills = st.session_state.get("nlp_extracted_job_skills", set())
        if nlp_extracted_job_skills:
            self._display_nlp_job_skills(nlp_extracted_job_skills)
    
    def _display_ai_job_skills(self, ai_extracted_job_skills: Dict, job_description_text: str) -> None:
        """Display AI-extracted job skills."""
        st.markdown("<b>AI-Extracted Job Requirements</b>", unsafe_allow_html=True)
        job_skill_headers = ["Skill", "Category", "Importance", "Required"]
        job_skill_rows = [
            [skill_name, skill_props.get("category", ""), skill_props.get("importance", ""), 
             "Yes" if skill_props.get("must_have") else "Preferred"]
            for skill_name, skill_props in ai_extracted_job_skills.items()
        ]
        job_skills_table_html = self._create_job_skills_table(job_skill_headers, job_skill_rows)
        st.markdown(job_skills_table_html, unsafe_allow_html=True)
        
        with st.expander("Detailed Job Analysis"):
            if "cached_job_analysis" not in st.session_state:
                st.session_state["cached_job_analysis"] = analyze_job_requirements(
                    job_description_text, ai_extracted_job_skills
                )
            st.info(st.session_state["cached_job_analysis"])
    
    def _display_nlp_job_skills(self, nlp_extracted_job_skills: Set) -> None:
        """Display NLP-extracted job skills."""
        st.markdown("<b>NLP-Extracted Job Requirements</b>", unsafe_allow_html=True)
        job_skill_headers = ["Skill"]
        job_skill_rows = [[skill_name] for skill_name in sorted(nlp_extracted_job_skills)]
        job_skills_table_html = self._create_job_skills_table(job_skill_headers, job_skill_rows)
        st.markdown(job_skills_table_html, unsafe_allow_html=True)
    
    def _create_job_skills_table(self, headers: list, rows: list) -> str:
        """Create HTML table for job skills."""
        return f"""
        <div class='professional-data-table'>
            <table>
                <thead>
                    <tr>
                        {''.join(f'<th>{header}</th>' for header in headers)}
                    </tr>
                </thead>
                <tbody>
                    {''.join(f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>" for row in rows)}
                </tbody>
            </table>
        </div>
        """
    
    def _render_job_analysis_comparison(self, job_description_text: str) -> None:
        """Render job analysis comparison table."""
        ai_input_sample = job_description_text[:2000]
        ai_output_sample = str(st.session_state["ai_extracted_job_skills"])
        estimated_cost, input_tokens, output_tokens = AnalysisUtilities.estimate_gpt4o_processing_cost(
            ai_input_sample, ai_output_sample
        )
        
        st.markdown("---")
        ProfessionalUIComponents.render_analysis_section_header("Analysis Comparison", "Job Analysis Comparison")
        ProfessionalUIComponents.render_professional_extraction_comparison_table(
            len(st.session_state['ai_extracted_job_skills']),
            st.session_state.get('ai_job_analysis_time', 0),
            len(st.session_state['nlp_extracted_job_skills']),
            st.session_state.get('nlp_job_analysis_time', 0),
            estimated_cost
        )
    
    def render_analysis_results_section(self) -> None:
        """Render the comprehensive analysis results section."""
        
        # Get processed data from previous steps
        extracted_resume_text = st.session_state.get("extracted_resume_text", "")
        job_description_text = st.session_state.get("job_description_text", "")
        ai_resume_skills = set(st.session_state.get("ai_extracted_resume_skills", {}).keys())
        ai_job_skills = set(st.session_state.get("ai_extracted_job_skills", {}).keys())
        nlp_resume_skills = st.session_state.get("nlp_extracted_resume_skills", set())
        nlp_job_skills = st.session_state.get("nlp_extracted_job_skills", set())

        # Initialize skill matching variables
        ai_matched_skills, ai_missing_skills, ai_extra_skills = set(), set(), set()
        nlp_matched_skills, nlp_missing_skills, nlp_extra_skills = set(), set(), set()
        similarity_score = None

        # Proceed with analysis if we have the required data
        if extracted_resume_text and job_description_text and ai_resume_skills and ai_job_skills:
            # Perform skill matching analysis
            ai_matched_skills, ai_missing_skills = perform_semantic_skill_matching(ai_resume_skills, ai_job_skills)
            ai_extra_skills = ai_resume_skills - ai_job_skills
            nlp_matched_skills, nlp_missing_skills = perform_semantic_skill_matching(nlp_resume_skills, nlp_job_skills)
            nlp_extra_skills = nlp_resume_skills - nlp_job_skills

            similarity_score = self._render_similarity_analysis(extracted_resume_text, job_description_text)
            self._render_skill_analysis_summary(ai_matched_skills, ai_missing_skills, ai_extra_skills, nlp_matched_skills, nlp_missing_skills, nlp_extra_skills)
            self._render_visualization_and_breakdown(ai_matched_skills, ai_missing_skills, ai_extra_skills)
            self._render_gap_analysis_and_export(ai_missing_skills, job_description_text, extracted_resume_text, similarity_score, ai_matched_skills)
        else:
            st.info("Please complete the resume upload and job description analysis before viewing results.")
            st.markdown("Navigate to the previous steps using the sidebar to begin your analysis.")
    
    def _render_similarity_analysis(self, extracted_resume_text: str, job_description_text: str) -> float:
        """Render the overall similarity analysis section and return the similarity score."""
        ProfessionalUIComponents.render_professional_numbered_header(1, "Overall Document Similarity Analysis")
        
        # Apply professional metric card styles
        st.markdown(get_metric_card_styles(), unsafe_allow_html=True)

        similarity_score = calculate_similarity_score(extracted_resume_text, job_description_text)
        if similarity_score is not None:
            # Calculate additional metrics for comprehensive analysis
            current_ai_resume_skills = set(st.session_state.get("ai_extracted_resume_skills", {}).keys())
            current_ai_job_skills = set(st.session_state.get("ai_extracted_job_skills", {}).keys())
            current_ai_matched, current_ai_missing = perform_semantic_skill_matching(
                current_ai_resume_skills, current_ai_job_skills
            )
            
            # Calculate metrics
            total_required = len(current_ai_job_skills)
            total_matched = len(current_ai_matched)
            coverage_pct = (total_matched / total_required * 100) if total_required > 0 else 0
            recommendation_score = (similarity_score * 0.6 + (coverage_pct/100) * 0.4) * 100
            
            # Create three columns for detailed similarity breakdown
            sim_col1, sim_col2, sim_col3 = st.columns(3)
            
            with sim_col1:
                self._render_overall_match_card(similarity_score)
            
            with sim_col2:
                self._render_skill_coverage_card(coverage_pct, total_matched, total_required)
            
            with sim_col3:
                self._render_hire_score_card(recommendation_score)
            
            st.caption("Advanced semantic analysis combining document similarity and skill coverage metrics.")
            
            return similarity_score
        
        return 0.0  # Return default score if calculation fails
    
    def _render_overall_match_card(self, similarity_score: float) -> None:
        """Render the overall match metric card."""
        if similarity_score > 0.75:
            match_badge = "Strong Match"
            color_primary = "#1976d2"
            color_secondary = "#42a5f5"
        elif similarity_score > 0.5:
            match_badge = "Good Match"
            color_primary = "#0072C6"
            color_secondary = "#64b5f6"
        else:
            match_badge = "Needs Improvement"
            color_primary = "#455a64"
            color_secondary = "#78909c"
            
        st.markdown(f"""
        <div class='professional-metric-card' style='
            background: linear-gradient(135deg, {color_primary} 0%, {color_secondary} 100%);
            color: white; 
            padding: 25px 20px; 
            border-radius: 12px; 
            text-align: center;
            box-shadow: 0 4px 20px rgba(25, 118, 210, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.2s ease-in-out;'>
            <h3 style='margin: 0 0 15px 0; color: white; font-weight: 600; font-size: 1.1rem; letter-spacing: 0.5px;'>Overall Match</h3>
            <div style='font-size: 2.8rem; font-weight: 700; margin: 15px 0; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>{similarity_score*100:.1f}%</div>
            <div style='font-size: 1rem; font-weight: 500; opacity: 0.95; letter-spacing: 0.3px;'>{match_badge}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_skill_coverage_card(self, coverage_pct: float, total_matched: int, total_required: int) -> None:
        """Render the skill coverage metric card."""
        coverage_color_primary = "#1976d2" if coverage_pct >= 75 else "#0072C6" if coverage_pct >= 50 else "#455a64"
        coverage_color_secondary = "#42a5f5" if coverage_pct >= 75 else "#64b5f6" if coverage_pct >= 50 else "#78909c"
        
        st.markdown(f"""
        <div class='professional-metric-card' style='
            background: linear-gradient(135deg, {coverage_color_primary} 0%, {coverage_color_secondary} 100%);
            color: white; 
            padding: 25px 20px; 
            border-radius: 12px; 
            text-align: center;
            box-shadow: 0 4px 20px rgba(25, 118, 210, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.2s ease-in-out;'>
            <h3 style='margin: 0 0 15px 0; color: white; font-weight: 600; font-size: 1.1rem; letter-spacing: 0.5px;'>Skill Coverage</h3>
            <div style='font-size: 2.8rem; font-weight: 700; margin: 15px 0; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>{coverage_pct:.1f}%</div>
            <div style='font-size: 1rem; font-weight: 500; opacity: 0.95; letter-spacing: 0.3px;'>{total_matched}/{total_required} Skills</div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_hire_score_card(self, recommendation_score: float) -> None:
        """Render the hire score metric card."""
        rec_text = "Highly Recommended" if recommendation_score >= 75 else "Good Candidate" if recommendation_score >= 60 else "Needs Development"
        rec_color_primary = "#1976d2" if recommendation_score >= 75 else "#0072C6" if recommendation_score >= 60 else "#455a64"
        rec_color_secondary = "#42a5f5" if recommendation_score >= 75 else "#64b5f6" if recommendation_score >= 60 else "#78909c"
        
        st.markdown(f"""
        <div class='professional-metric-card' style='
            background: linear-gradient(135deg, {rec_color_primary} 0%, {rec_color_secondary} 100%);
            color: white; 
            padding: 25px 20px; 
            border-radius: 12px; 
            text-align: center;
            box-shadow: 0 4px 20px rgba(25, 118, 210, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.2s ease-in-out;'>
            <h3 style='margin: 0 0 15px 0; color: white; font-weight: 600; font-size: 1.1rem; letter-spacing: 0.5px;'>Hire Score</h3>
            <div style='font-size: 2.8rem; font-weight: 700; margin: 15px 0; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>{recommendation_score:.0f}</div>
            <div style='font-size: 1rem; font-weight: 500; opacity: 0.95; letter-spacing: 0.3px;'>{rec_text}</div>
        </div>
        """, unsafe_allow_html=True)

    def _render_skill_analysis_summary(self, ai_matched: set, ai_missing: set, ai_extra: set, nlp_matched: set, nlp_missing: set, nlp_extra: set) -> None:
        """Render the detailed skill analysis summary."""
        ProfessionalUIComponents.render_professional_numbered_header(2, "Detailed Skill Analysis Summary")
        ProfessionalUIComponents.render_professional_skill_summary_table(
            len(ai_matched), len(ai_missing), len(ai_extra),
            len(nlp_matched), len(nlp_missing), len(nlp_extra)
        )

    def _render_visualization_and_breakdown(self, ai_matched: set, ai_missing: set, ai_extra: set) -> None:
        """Render the visualization and interactive skill breakdown."""
        ProfessionalUIComponents.render_professional_dual_section_header(
            "3", "Skill Distribution Visualization", "",
            "4", "Interactive Skill Breakdown", ""
        )
        
        visualization_column, interaction_column = st.columns(2)

        # Skill distribution pie chart
        with visualization_column:
            skill_distribution_chart = px.pie(
                names=["Matched", "Missing", "Additional"],
                values=[len(ai_matched), len(ai_missing), len(ai_extra)],
                title="Skill Coverage Analysis",
                color_discrete_sequence=["#4CAF50", "#FF5252", "#00B8D9"]
            )
            skill_distribution_chart.update_traces(
                textinfo="percent+label",
                pull=[0.10, 0.07, 0.04],
                marker=dict(line=dict(color='#fff', width=3)),
                opacity=0.96,
                hoverinfo="label+percent+value"
            )
            skill_distribution_chart.update_layout(
                title_font_size=22,
                font=dict(family="Segoe UI, Arial", size=17, color="#222"),
                paper_bgcolor="rgba(246,248,250,0.95)",
                plot_bgcolor="rgba(246,248,250,0.95)",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.18,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=16)
                ),
                margin=dict(t=50, b=30, l=0, r=0),
                showlegend=True
            )
            st.plotly_chart(skill_distribution_chart, use_container_width=True)

        # Interactive skill exploration
        with interaction_column:
            self._render_interactive_skill_explorer(ai_matched, ai_missing, ai_extra)

    def _render_interactive_skill_explorer(self, ai_matched: set, ai_missing: set, ai_extra: set) -> None:
        """Render the interactive skill explorer."""
        st.markdown(get_radio_button_styles(), unsafe_allow_html=True)

        skill_view_options = ["Matched Skills", "Missing Skills", "Additional Skills"]
        selected_skill_view = st.radio(
            "Select skill category to explore:",
            skill_view_options,
            horizontal=True,
            key="skill_category_selector"
        )

        if selected_skill_view == "Matched Skills":
            st.markdown("<b>Skills Present in Both Resume and Job Description:</b>", unsafe_allow_html=True)
            if ai_matched:
                skill_cards_html = "".join([
                    ProfessionalUIComponents.create_professional_skill_card(skill, "matched") 
                    for skill in sorted(ai_matched)
                ])
                st.markdown(skill_cards_html, unsafe_allow_html=True)
            else:
                st.info("No matching skills identified between resume and job requirements.")
                
        elif selected_skill_view == "Missing Skills":
            st.markdown("<b>Required Skills Not Found in Resume:</b>", unsafe_allow_html=True)
            if ai_missing:
                skill_cards_html = "".join([
                    ProfessionalUIComponents.create_professional_skill_card(skill, "missing") 
                    for skill in sorted(ai_missing)
                ])
                st.markdown(skill_cards_html, unsafe_allow_html=True)
            else:
                st.success("All required skills are present in the resume.")
                
        else:
            st.markdown("<b>Additional Skills in Resume (Not Required by Job):</b>", unsafe_allow_html=True)
            if ai_extra:
                skill_cards_html = "".join([
                    ProfessionalUIComponents.create_professional_skill_card(skill, "extra") 
                    for skill in sorted(ai_extra)
                ])
                st.markdown(skill_cards_html, unsafe_allow_html=True)
            else:
                st.info("No additional skills beyond job requirements found in resume.")

        st.caption("Skills are analyzed using advanced AI processing. Use the options above to explore different skill categories.")

    def _render_gap_analysis_and_export(self, ai_missing: set, job_description_text: str, extracted_resume_text: str, similarity_score: float, ai_matched: set) -> None:
        """Render the skill gap analysis and export reports section."""
        ProfessionalUIComponents.render_professional_dual_section_header(
            "5", "Comprehensive Skill Gap Analysis", "",
            "6", "Export Comprehensive Reports", ""
        )
        
        gap_analysis_column, export_column = st.columns(2)
        
        # Left column: Skill Gap Analysis & Recommendations
        with gap_analysis_column:
            if ai_missing:
                st.markdown("<b>Professional Development Recommendations</b>", unsafe_allow_html=True)
                
                for skill_index, missing_skill in enumerate(sorted(ai_missing), 1):
                    skill_recommendation = PROFESSIONAL_SKILL_RECOMMENDATIONS.get(missing_skill, {})
                    recommendation_section = f"{skill_index}. {missing_skill.title()}"
                    
                    with st.expander(recommendation_section, expanded=False):
                        st.markdown(get_expandable_content_styles(), unsafe_allow_html=True)
                        st.write(f"**Priority Level:** High")
                        
                        # Generate comprehensive AI analysis (combines analysis + recommendations)
                        comprehensive_analysis_cache_key = f"comprehensive_skill_analysis_{missing_skill}"
                        if comprehensive_analysis_cache_key not in st.session_state:
                            try:
                                with st.spinner(f"Generating comprehensive analysis for {missing_skill}..."):
                                    comprehensive_prompt = f"""
                                    Provide a comprehensive analysis and recommendation for the missing skill: {missing_skill}
                                    
                                    Context: 
                                    - This skill is required for the job but missing from the candidate's resume
                                    - Candidate's current skills: {', '.join(sorted(ai_matched))}
                                    - Job context: {job_description_text[:500]}...
                                    
                                    Please provide a concise response covering:
                                    1. Why this skill is important for the role
                                    2. Priority level (High/Medium/Low) 
                                    3. Estimated learning time
                                    4. Specific learning path and actionable recommendations
                                    5. How it connects to existing skills
                                    
                                    Keep the response professional and actionable, suitable for career development planning.
                                    """
                                    
                                    # Use the single skill recommendation function for individual skill analysis
                                    comprehensive_analysis = get_single_skill_recommendation(missing_skill, comprehensive_prompt)
                                    st.session_state[comprehensive_analysis_cache_key] = comprehensive_analysis
                            except Exception as e:
                                st.session_state[comprehensive_analysis_cache_key] = "AI analysis temporarily unavailable."
                        
                        # Display comprehensive AI analysis
                        comprehensive_analysis = st.session_state.get(comprehensive_analysis_cache_key, "")
                        if (comprehensive_analysis and 
                            comprehensive_analysis not in ["No specific recommendation available.", "AI analysis temporarily unavailable.", ""] and
                            len(comprehensive_analysis.strip()) > 10):
                            
                            # Clean up the AI response by removing markdown formatting for better display
                            clean_analysis = re.sub(r'#{1,6}\s*(.+)', r'**\1**', comprehensive_analysis)
                            
                            st.success("**AI-Powered Analysis & Recommendations:**")
                            st.info(clean_analysis)
                        
                        # Display predefined recommendations if available
                        if skill_recommendation and skill_recommendation.get("desc"):
                            st.success("**Additional Learning Resource:**")
                            st.info(skill_recommendation.get("desc", "No detailed description available."))
                            if skill_recommendation.get("link"):
                                st.markdown(f"[Learn More]({skill_recommendation['link']})")
            else:
                st.success("No skill gaps identified. Candidate qualifications align with position requirements.")

        # Right column: Export Reports
        with export_column:
            self._render_export_options(similarity_score, ai_matched, ai_missing, extracted_resume_text, job_description_text)

    def _render_export_options(self, similarity_score: float, ai_matched: set, ai_missing: set, extracted_resume_text: str, job_description_text: str) -> None:
        """Render the export options section."""
        st.markdown("<b>Download Analysis Reports</b>", unsafe_allow_html=True)
        st.markdown(get_download_button_styles(), unsafe_allow_html=True)

        # Center the export buttons
        st.markdown('<div class="download-button-container">', unsafe_allow_html=True)
        
        # CSV Report
        analysis_csv_data = generate_analysis_report(similarity_score, ai_matched, ai_missing)
        st.download_button(
            "Download CSV Report", 
            data=analysis_csv_data, 
            file_name="resume_analysis_report.csv", 
            mime="text/csv", 
            use_container_width=True
        )
        
        # PDF Report
        if extracted_resume_text and job_description_text and ai_matched and ai_missing: 
            # Use cached analysis results to avoid unnecessary API calls
            cached_job_analysis = st.session_state.get("cached_job_analysis", "No job analysis available")
            cached_resume_analysis = st.session_state.get("cached_resume_analysis", "No resume analysis available")
            
            comprehensive_html_report = generate_html_report(
                resume_name="Professional Resume",
                jd_summary=job_description_text[:300] + ("..." if len(job_description_text) > 300 else ""),
                score=similarity_score,
                matched=ai_matched,
                missing=ai_missing,
                job_insights=cached_job_analysis,
                resume_insights=cached_resume_analysis
            )
            
            pdf_report_path = create_pdf_analysis_report(comprehensive_html_report)
            with open(pdf_report_path, "rb") as pdf_file:
                st.download_button(
                    "Download PDF Report", 
                    pdf_file, 
                    file_name="comprehensive_analysis_report.pdf", 
                    mime="application/pdf", 
                    use_container_width=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional export information
        st.info("**Export Options:**\n\n"
               "• **CSV Report**: Detailed data for spreadsheet analysis\n\n"
               "• **PDF Report**: Professional document for sharing")
