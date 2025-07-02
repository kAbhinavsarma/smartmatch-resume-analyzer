"""
SmartMatch Resume Analyzer - Main Application

A comprehensive resume analysis tool that compares resumes against job descriptions
using both traditional NLP and modern AI techniques. Provides detailed skill matching,
gap analysis, and hiring recommendations for recruiters and job seekers.

Author: Resume Analysis Team
Version: 1.0.0
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from the project root directory
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Configuration imports
from config.settings import APPLICATION_CONFIG

# UI and workflow imports
from streamlit_option_menu import option_menu
from src.ui.styles import get_main_application_styles
from src.ui.workflow_components import WorkflowComponents

# Initialize modular components
workflow_ui = WorkflowComponents()

# Configure Streamlit page settings
st.set_page_config(
    page_title=APPLICATION_CONFIG["title"],
    layout=APPLICATION_CONFIG["layout"],
    page_icon=APPLICATION_CONFIG["page_icon"],
    initial_sidebar_state=APPLICATION_CONFIG["initial_sidebar_state"]
)

# Apply global styling
st.markdown(get_main_application_styles(), unsafe_allow_html=True)

# Initialize session state for navigation - FIXED VERSION
if 'navigation_initialized' not in st.session_state:
    st.session_state.navigation_initialized = True
    st.session_state.selected_page = "Upload Resume"

# Main application header
st.title("SmartMatch: Professional Resume & Job Description Analyzer")
st.caption("Advanced resume analysis platform that compares candidate qualifications against job requirements. "
          "Provides detailed skill matching, gap identification, and actionable recommendations. "
          "Powered by modern NLP and AI technology.")

# Navigation sidebar - PROPER FIX for option_menu caching issue
with st.sidebar:
    # Clear any existing menu state first
    if 'menu_created' not in st.session_state:
        st.session_state.menu_created = True
    
    # Force fresh menu creation each time with proper state management
    pages = ["Upload Resume", "Job Description", "Analysis Results"]
    current_index = pages.index(st.session_state.selected_page)
    
    # Create the menu with manual_select to avoid caching issues
    selected = option_menu(
        menu_title="Analysis Workflow",
        options=pages,
        icons=["upload", "file-text", "bar-chart"],
        menu_icon="cast",
        default_index=current_index,
        orientation="vertical",
        manual_select=current_index,  # This fixes the caching issue
        key=None,  # Don't use persistent keys
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#1976d2", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#1976d2"},
        }
    )
    
    # Update state only when selection actually changes
    if selected != st.session_state.selected_page:
        st.session_state.selected_page = selected
        st.rerun()
    
    current_page = st.session_state.selected_page

# Progress indicator for workflow steps
workflow_progress = {"Upload Resume": 33, "Job Description": 66, "Analysis Results": 100}
st.progress(workflow_progress[current_page])

# STEP 1: RESUME UPLOAD AND SKILL EXTRACTION
if current_page == "Upload Resume":
    workflow_ui.render_resume_upload_section()

# STEP 2: JOB DESCRIPTION ANALYSIS
elif current_page == "Job Description":
    workflow_ui.render_job_description_section()

# STEP 3: COMPREHENSIVE ANALYSIS AND RESULTS
elif current_page == "Analysis Results":
    workflow_ui.render_analysis_results_section()
