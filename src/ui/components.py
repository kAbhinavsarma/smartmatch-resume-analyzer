"""
Professional UI Components for Resume Analysis Application

This module provides enterprise-grade, reusable UI components for the Streamlit-based
resume analysis application. Components are designed for professional recruitment
workflows with clean, consistent styling and comprehensive functionality.

Classes:
    ProfessionalUIComponents: Main collection of UI components for analysis interface

Functions:
    - create_professional_table: Generate HTML tables with enterprise styling
    - render_analysis_section: Display analysis sections with professional formatting
    - render_skill_comparison: Present skill comparison results
    - render_progress_indicator: Show workflow progress to users
    - render_recommendation_panel: Display skill development recommendations

Author: Resume Analysis Team
Version: 1.0.0
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Set, Any, Tuple, List, Optional
from src.ui.styles import get_section_header, get_gradient_box
from config.settings import THEME_CONFIG

class ProfessionalUIComponents:
    """
    Enterprise-grade UI components for professional resume analysis interface.
    
    Provides comprehensive, reusable components designed for recruitment workflows
    with consistent styling, accessibility, and professional presentation standards.
    """
    
    @staticmethod
    def create_professional_html_table(headers: List[str], rows: List[List[str]], 
                                     table_class: str = "professional-data-table") -> str:
        """
        Create professionally styled HTML table with enterprise formatting.
        
        Args:
            headers: Column headers for the table
            rows: Data rows, each row is a list of cell values
            table_class: CSS class for styling customization
            
        Returns:
            Professional HTML table string with proper accessibility attributes
        """
        # Build header row
        header_html = ''.join(f'<th role="columnheader" scope="col">{header}</th>' for header in headers)
        
        # Build data rows  
        rows_html = ''
        for row in rows:
            cells_html = ''.join(f'<td role="gridcell">{cell}</td>' for cell in row)
            rows_html += f'<tr role="row">{cells_html}</tr>'
        
        table_html = f"""
        <div class='{table_class}' role='table' aria-label='Analysis Results'>
            <table>
                <thead>
                    <tr role='row'>{header_html}</tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """
        return table_html
    
    @staticmethod
    def render_analysis_section_header(title: str, description: Optional[str] = None):
        """
        Render professional section header with consistent formatting.
        
        Args:
            title: Primary section title
            description: Optional detailed description for context
        """
        st.markdown(f"<h2 class='section-title'>{title}</h2>", unsafe_allow_html=True)
        if description:
            st.markdown(
                f"<div class='section-description'>{description}</div>", 
                unsafe_allow_html=True
            )
    
    @staticmethod
    def render_skill_extraction_interface(section_title: str, extraction_button_text: str, 
                                        button_key: str, skills_data: Any, 
                                        processing_time: Optional[float] = None) -> bool:
        """
        Render professional skill extraction interface with results display.
        
        Args:
            section_title: Title for the extraction section
            extraction_button_text: Text for the extraction trigger button
            button_key: Unique key for button state management
            skills_data: Extracted skills data (dict for AI, set/list for NLP)
            processing_time: Optional processing time for performance metrics
            
        Returns:
            Boolean indicating if extraction button was clicked
        """
        st.markdown(f"<h3 class='subsection-title'>{section_title}</h3>", unsafe_allow_html=True)
        
        extraction_triggered = st.button(extraction_button_text, key=button_key, use_container_width=True)
        
        if skills_data:
            if isinstance(skills_data, dict):
                # Handle AI-extracted skills with comprehensive metadata
                headers = ["Skill Name", "Category", "Proficiency Level"]
                rows = [
                    [skill, props.get("category", "General"), props.get("importance", "Standard")]
                    for skill, props in skills_data.items()
                ]
                table_html = ProfessionalUIComponents.create_professional_html_table(headers, rows)
                st.markdown(table_html, unsafe_allow_html=True)
            elif isinstance(skills_data, (set, list)):
                # Handle NLP-extracted skills with basic presentation
                headers = ["Skill Name"]
                rows = [[skill] for skill in sorted(skills_data)]
                table_html = ProfessionalUIComponents.create_professional_html_table(headers, rows)
                st.markdown(table_html, unsafe_allow_html=True)
            
            if processing_time:
                st.caption(f"Processing completed in {processing_time:.2f} seconds")
        
        return extraction_triggered
    
    @staticmethod
    def render_professional_comparison_table(ai_data: Dict, nlp_data: Set, 
                                           ai_time: float, nlp_time: float, cost: str):
        """
        Render comprehensive comparison between AI and NLP extraction methodologies.
        
        Args:
            ai_data: AI extraction results with metadata
            nlp_data: NLP extraction results (basic skill list)
            ai_time: Processing time for AI extraction
            nlp_time: Processing time for NLP extraction
            cost: Estimated cost for AI processing
        """
        comparison_data = [
            ["AI Analysis (GPT-4)", len(ai_data), f"{ai_time:.2f}", cost, "Comprehensive"],
            ["NLP Processing", len(nlp_data), f"{nlp_time:.2f}", "No Cost", "Basic"]
        ]
        
        headers = ["Analysis Method", "Skills Identified", "Processing Time (sec)", "Cost per Analysis", "Metadata Available"]
        
        table_html = ProfessionalUIComponents.create_professional_html_table(headers, comparison_data)
        st.markdown(table_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_skill_match_visualization(matched_skills: Set[str], missing_skills: Set[str], 
                                       additional_skills: Set[str]) -> go.Figure:
        """
        Create professional skill match visualization for analysis results.
        
        Args:
            matched_skills: Skills found in both resume and job description
            missing_skills: Skills required but not found in resume
            additional_skills: Skills in resume but not required by job
            
        Returns:
            Professional Plotly figure for skill distribution analysis
        """
        categories = ['Skills Matched', 'Skills Missing', 'Additional Skills']
        values = [len(matched_skills), len(missing_skills), len(additional_skills)]
        colors = [THEME_CONFIG["success_color"], THEME_CONFIG["warning_color"], THEME_CONFIG["info_color"]]
        
        fig = go.Figure(data=[go.Pie(
            labels=categories, 
            values=values, 
            hole=0.6,
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='label+percent',
            textfont=dict(size=14, family="Arial"),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text="Professional Skill Match Analysis", 
                x=0.5, 
                font=dict(size=18, family="Arial", color="#2c3e50")
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
            height=400,
            margin=dict(t=60, b=40, l=40, r=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def render_workflow_progress(current_step: int, total_steps: int = 3):
        """
        Display professional workflow progress indicator.
        
        Args:
            current_step: Current step in the analysis workflow
            total_steps: Total number of steps in the process
        """
        progress_percentage = (current_step / total_steps)
        st.progress(progress_percentage)
        st.caption(f"Analysis Progress: Step {current_step} of {total_steps}")
    
    @staticmethod
    def create_professional_skill_card(skill_name: str, skill_status: str) -> str:
        """
        Generate professional HTML for skill status display.
        
        Args:
            skill_name: Name of the skill
            skill_status: Status indicator ('matched', 'missing', 'additional')
            
        Returns:
            Professional HTML string for skill card
        """
        status_config = {
            "matched": {"color": "#e8f5e9", "border": "#4caf50", "icon": "✓"},
            "missing": {"color": "#fff3e0", "border": "#ff9800", "icon": "!"},
            "additional": {"color": "#e3f2fd", "border": "#2196f3", "icon": "+"}
        }
        
        config = status_config.get(skill_status, status_config["matched"])
        
        return f"""
            <div style='display:inline-block;background:{config["color"]};
                        border:1px solid {config["border"]};border-radius:6px;
                        padding:8px 16px;margin:4px;font-size:14px;
                        font-weight:500;color:#2c3e50;'>
                <span style='font-weight:600;margin-right:4px;'>{config["icon"]}</span>
                {skill_name.title()}
            </div>
        """
    


    @staticmethod
    def render_professional_metric_card(score: float):
        """
        Render professional metric card with score and assessment indicator.
        
        Args:
            score: Similarity score between 0 and 1
        """
        if score > 0.75:
            badge_color = "#4caf50"
            badge_text = "Strong Match"
            status_indicator = "High Compatibility"
        elif score > 0.5:
            badge_color = "#ff9800" 
            badge_text = "Moderate Match"
            status_indicator = "Partial Compatibility"
        else:
            badge_color = "#f44336"
            badge_text = "Weak Match"
            status_indicator = "Limited Compatibility"
            
        st.markdown(
            f"""
            <div class="professional-metric-card">
                <div class="metric-content">
                    <div class="metric-label">Semantic Similarity Score</div>
                    <div class="metric-score">{score*100:.1f}%</div>
                </div>
                <div class="metric-badge" style="background-color:{badge_color};">
                    <span class="badge-text">{badge_text}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(score)
        st.caption("Calculated using advanced semantic similarity algorithms (SBERT embeddings)")

    @staticmethod
    def render_professional_skill_highlights(matched_skills: Set[str], missing_skills: Set[str], additional_skills: Set[str]):
        """
        Render professional skill highlight interface with category selection.
        
        Args:
            matched_skills: Skills found in both resume and job description
            missing_skills: Skills required but not found in resume
            additional_skills: Skills in resume but not required by job
        """
        st.markdown("""
        <style>
        .skill-category-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .skill-category-button {
            padding: 8px 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #f8f9fa;
            cursor: pointer;
            font-weight: 500;
        }
        .skill-category-button.active {
            background: #1976d2;
            color: white;
            border-color: #1976d2;
        }
        </style>
        """, unsafe_allow_html=True)
        
        highlight_options = ["Skills Matched", "Skills Missing", "Additional Skills"]
        selected_category = st.radio(
            "Skill Category Analysis:",
            highlight_options,
            horizontal=True,
            key="skill_highlight_mode"
        )
        
        if selected_category == "Skills Matched":
            st.markdown("<h4>Skills Successfully Matched</h4>", unsafe_allow_html=True)
            if matched_skills:
                skill_cards = [
                    ProfessionalUIComponents.create_professional_skill_card(skill, "matched") 
                    for skill in sorted(matched_skills)
                ]
                st.markdown("".join(skill_cards), unsafe_allow_html=True)
            else:
                st.info("No matching skills identified in the analysis.")
                
        elif selected_category == "Skills Missing":
            st.markdown("<h4>Skills Requiring Development</h4>", unsafe_allow_html=True)
            if missing_skills:
                skill_cards = [
                    ProfessionalUIComponents.create_professional_skill_card(skill, "missing") 
                    for skill in sorted(missing_skills)
                ]
                st.markdown("".join(skill_cards), unsafe_allow_html=True)
            else:
                st.success("All required skills are present in the candidate's profile.")
                
        else:
            st.markdown("<h4>Additional Skills Beyond Job Requirements</h4>", unsafe_allow_html=True)
            if additional_skills:
                skill_cards = [
                    ProfessionalUIComponents.create_professional_skill_card(skill, "additional") 
                    for skill in sorted(additional_skills)
                ]
                st.markdown("".join(skill_cards), unsafe_allow_html=True)
            else:
                st.info("No additional skills identified beyond job requirements.")
                
        st.caption("Skills are analyzed using advanced AI processing. Toggle between categories to view different skill classifications.")
    
    @staticmethod
    def render_professional_extraction_comparison_table(ai_count: int, ai_time: float, 
                                                       nlp_count: int, nlp_time: float, cost: str):
        """
        Render comprehensive comparison between AI and NLP extraction methodologies.
        
        Args:
            ai_count: Number of skills identified by AI analysis
            ai_time: Processing time for AI extraction
            nlp_count: Number of skills identified by NLP processing
            nlp_time: Processing time for NLP extraction
            cost: Estimated cost for AI processing
        """
        headers = [
            "Analysis Method", "Skills Identified", "Processing Time", "Cost per Analysis", 
            "Skill Categorization", "Context Analysis", "Accuracy Level", 
            "Metadata Richness", "Scalability", "Optimal Use Case"
        ]
        rows = [
            [
                "AI Analysis (GPT-4)", 
                f"{ai_count} skills", 
                f"{ai_time:.2f}s", 
                cost,
                "Automated categorization",
                "Deep contextual understanding",
                "95%+ precision",
                "Comprehensive (importance, priority flags)",
                "Cost scales with usage",
                "Detailed candidate evaluation"
            ],
            [
                "NLP Processing", 
                f"{nlp_count} skills", 
                f"{nlp_time:.2f}s", 
                "No cost",
                "Manual categorization required",
                "Pattern-based matching",
                "80-85% precision",
                "Basic (skill names only)",
                "Unlimited free processing",
                "High-volume initial screening"
            ]
        ]
        
        table_html = ProfessionalUIComponents.create_professional_html_table(headers, rows)
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Add professional explanation for recruitment teams
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    border-radius: 8px; padding: 20px; margin: 16px 0; 
                    border-left: 4px solid #1976d2;'>
            <h4 style='color: #1976d2; margin-top: 0; font-weight: 600;'>Strategic Implementation for Recruitment Teams</h4>
            <p><strong>AI Analysis:</strong> Optimal for comprehensive candidate evaluation, skill relevance assessment, and generating detailed interview insights.</p>
            <p><strong>NLP Processing:</strong> Ideal for high-volume resume screening, rapid skill identification, and cost-effective bulk candidate processing.</p>
            <p><strong>Recommended Workflow:</strong> Utilize NLP for initial candidate screening (100+ applications), then apply AI analysis for final candidate evaluation (top 15-20 candidates).</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_professional_numbered_header(section_number: int, section_title: str):
        """
        Render professional numbered section header with consistent styling.
        
        Args:
            section_number: Sequential section number
            section_title: Descriptive section title
        """
        st.markdown(f"""
            <div style='display:flex;align-items:center;gap:12px;margin-bottom:12px;'>
                <span style='background:#1976d2;color:#fff;font-weight:600;border-radius:50%;
                            width:36px;height:36px;display:inline-flex;align-items:center;
                            justify-content:center;font-size:18px;'>{section_number}</span>
                <span style='font-size:24px;font-weight:600;color:#2c3e50;'>{section_title}</span>
            </div>
            <hr style="border:none;border-top:2px solid #e0e0e0;margin:0 0 20px 0;">
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_professional_skill_summary_table(ai_matched: int, ai_missing: int, ai_additional: int, 
                                              nlp_matched: int, nlp_missing: int, nlp_additional: int):
        """
        Render comprehensive skill analysis summary table for recruitment decisions.
        
        Args:
            ai_matched: Number of AI-identified matched skills
            ai_missing: Number of AI-identified missing skills
            ai_additional: Number of AI-identified additional skills
            nlp_matched: Number of NLP-identified matched skills
            nlp_missing: Number of NLP-identified missing skills
            nlp_additional: Number of NLP-identified additional skills
        """
        ai_total = ai_matched + ai_missing + ai_additional
        nlp_total = nlp_matched + nlp_missing + nlp_additional
        
        # Calculate match rates based on required skills only (matched + missing)
        # Exclude additional skills from denominator as they exceed job requirements
        ai_required = ai_matched + ai_missing
        nlp_required = nlp_matched + nlp_missing
        
        ai_match_rate = (ai_matched / ai_required * 100) if ai_required > 0 else 0
        nlp_match_rate = (nlp_matched / nlp_required * 100) if nlp_required > 0 else 0
        
        headers = [
            "Analysis Method", "Skills Matched", "Skills Missing", "Additional Skills", "Total Skills", 
            "Match Rate", "Coverage Quality", "Recruitment Confidence"
        ]
        rows = [
            [
                "AI Analysis (GPT-4)", 
                ai_matched, 
                ai_missing, 
                ai_additional, 
                ai_total,
                f"{ai_match_rate:.1f}%",
                "Context-aware skill matching",
                "High - comprehensive skill depth analysis"
            ],
            [
                "NLP Processing", 
                nlp_matched, 
                nlp_missing, 
                nlp_additional, 
                nlp_total,
                f"{nlp_match_rate:.1f}%",
                "Keyword-based skill identification",
                "Medium - surface-level skill detection"
            ]
        ]
        
        table_html = ProfessionalUIComponents.create_professional_html_table(headers, rows)
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Generate professional recruitment insights
        recommended_method = "AI Analysis" if ai_match_rate > nlp_match_rate else "NLP Processing"
        confidence_level = "High" if ai_match_rate > 70 else "Medium" if ai_match_rate > 50 else "Requires Review"
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #e8f5e9 0%, #f3e5f5 100%); 
                    border-radius: 8px; padding: 20px; margin: 16px 0; 
                    border-left: 4px solid #4caf50;'>
            <h4 style='color: #2e7d32; margin-top: 0; font-weight: 600;'>Recruitment Decision Support</h4>
            <p><strong>Recommended Analysis Method:</strong> {recommended_method} provides superior skill coverage assessment for this candidate.</p>
            <p><strong>Hiring Confidence Level:</strong> {confidence_level} based on {ai_match_rate:.1f}% match rate for required competencies.</p>
            <p><strong>Next Action Items:</strong> {"Conduct targeted interviews focusing on missing skills and validate additional competencies." if ai_missing > 0 else "Proceed with technical assessment - strong skill alignment confirmed."}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_professional_gradient_box(content: str, start_color: str, end_color: str, angle: int = 135):
        """
        Render professional gradient box with custom styling.
        
        Args:
            content: HTML content to display in the box
            start_color: Starting color of gradient
            end_color: Ending color of gradient
            angle: Gradient angle in degrees
        """
        st.markdown(get_gradient_box(content, start_color, end_color, angle), unsafe_allow_html=True)
    
    @staticmethod
    def render_professional_dual_section_header(primary_number: str, primary_title: str, primary_subtitle: str, 
                                              secondary_number: str, secondary_title: str, secondary_subtitle: str):
        """
        Render professional dual section header with two sections displayed side by side.
        
        Args:
            primary_number: First section identifier number
            primary_title: First section main title
            primary_subtitle: First section descriptive subtitle
            secondary_number: Second section identifier number
            secondary_title: Second section main title
            secondary_subtitle: Second section descriptive subtitle
        """
        from src.ui.styles import get_dual_header_styles
        st.markdown(get_dual_header_styles(), unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="dual-header-row">
            <div class="dual-header-section">
                <span class="dual-header-badge">{primary_number}</span>
                <span class="dual-header-title">{primary_title} <span style="color:#1976d2;">{primary_subtitle}</span></span>
            </div>
            <div class="dual-header-section">
                <span class="dual-header-badge">{secondary_number}</span>
                <span class="dual-header-title">{secondary_title} <span style="color:#1976d2;">{secondary_subtitle}</span></span>
            </div>
        </div>
        <hr style="border:none;border-top:2px solid #e0e0e0;margin:0 0 20px 0;">
        """, unsafe_allow_html=True)


# Simple alias for backward compatibility - using the professional class
UIComponents = ProfessionalUIComponents
