"""
CSS styles and theme configurations for the Streamlit application.
"""
from config.settings import THEME_CONFIG

def get_main_styles() -> str:
    """Get the main CSS styles for the application."""
    return f"""
    <style>
        .block-container {{
            padding-top: 2rem;
        }}
        .stDataFrame {{
            background: #f9f9f9;
            border-radius: 12px;
            border: 1px solid #e3e3e3;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        .stDataFrame > div {{
            border-radius: 12px;
        }}
        
        /* Style the dataframe table headers */
        .stDataFrame table thead th {{
            background: {THEME_CONFIG["primary_brand_color"]} !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1.05em !important;
            padding: 0.8em !important;
            text-align: left !important;
            border: none !important;
        }}
        
        /* Style the dataframe table cells */
        .stDataFrame table tbody td {{
            padding: 0.7em 0.8em !important;
            border-bottom: 1px solid #f0f0f0 !important;
            font-size: 1rem !important;
            background: white !important;
        }}
        
        /* Hover effect for table rows */
        .stDataFrame table tbody tr:hover td {{
            background: #f8f9fa !important;
        }}
        .stButton>button {{
            width: 100%;
        }}
        .css-1aumxhk {{
            font-size: 1.1rem;
        }}
        .stExpanderHeader {{
            font-weight: bold;
        }}
        
        /* Custom gradient backgrounds */
        .gradient-header {{
            background: {THEME_CONFIG["background_gradient"]};
            border-radius: 14px;
            padding: 0.7em 1.1em;
            margin-bottom: 1em;
            box-shadow: 0 2px 12px {THEME_CONFIG["primary_brand_color"]}10;
        }}
        
        /* Comparison table styles */
        .professional-legacy-table {{
            margin-top: 0.5em;
            margin-bottom: 1.2em;
            border-radius: 16px;
            overflow: auto;
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
            border: 1px solid #e3e3e3;
        }}
        
        .professional-legacy-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .professional-legacy-table th {{
            background: {THEME_CONFIG["primary_brand_color"]};
            color: white;
            padding: 1em;
            text-align: left;
            font-weight: 600;
            font-size: 1.05em;
        }}
        
        .professional-legacy-table td {{
            padding: 0.8em 1em;
            border-bottom: 1px solid #f0f0f0;
            font-size: 1rem;
        }}
        
        .professional-legacy-table tr:hover {{
            background-color: #f8f9fa;
        }}
        
        /* Professional data table styling with horizontal scroll */
        .professional-data-table {{
            background: white;
            border-radius: 12px;
            border: 1px solid #e3e3e3;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow-x: auto;
            overflow-y: hidden;
            margin: 1rem 0;
            width: 100%;
            position: relative;
        }}
        
        /* Custom scrollbar styling */
        .professional-data-table::-webkit-scrollbar {{
            height: 8px;
        }}
        
        .professional-data-table::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        .professional-data-table::-webkit-scrollbar-thumb {{
            background: {THEME_CONFIG["primary_brand_color"]};
            border-radius: 4px;
        }}
        
        .professional-data-table::-webkit-scrollbar-thumb:hover {{
            background: #0052a3;
        }}
        
        .professional-data-table table {{
            width: max-content;
            min-width: 100%;
            border-collapse: collapse;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            table-layout: fixed;
        }}
        
        .professional-data-table th {{
            background: {THEME_CONFIG["primary_brand_color"]};
            color: white;
            padding: 0.8rem 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            border: none;
            white-space: nowrap;
            min-width: 140px;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .professional-data-table th:first-child {{
            min-width: 160px;
            position: sticky;
            left: 0;
            z-index: 11;
        }}
        
        .professional-data-table td {{
            padding: 0.7rem 1rem;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.85rem;
            line-height: 1.4;
            background: white;
            vertical-align: top;
            white-space: nowrap;
            min-width: 140px;
        }}
        
        .professional-data-table td:first-child {{
            min-width: 160px;
            position: sticky;
            left: 0;
            background: white;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            font-weight: 600;
            color: {THEME_CONFIG["primary_brand_color"]};
        }}
        
        .professional-data-table tr:nth-child(even) td {{
            background: #f8f9fa;
        }}
        
        .professional-data-table tr:nth-child(even) td:first-child {{
            background: #f8f9fa;
        }}
        
        .professional-data-table tr:hover td {{
            background: #e3f2fd !important;
        }}
        
        .professional-data-table tr:hover td:first-child {{
            background: #e3f2fd !important;
        }}
        
        /* Scroll hint for users */
        .professional-data-table::after {{
            content: "← Scroll horizontally to view all columns →";
            position: absolute;
            bottom: -25px;
            right: 0;
            font-size: 0.75rem;
            color: #666;
            font-style: italic;
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .professional-data-table th,
            .professional-data-table td {{
                padding: 0.5rem 0.8rem;
                font-size: 0.8rem;
                min-width: 120px;
            }}
            
            .professional-data-table th:first-child,
            .professional-data-table td:first-child {{
                min-width: 140px;
            }}
        }}
        
        /* Download button styles */
        .download-btn-row {{
            display: flex;
            flex-direction: row;
            gap: 1.1em;
            margin-top: 0.5em;
            margin-bottom: 1.5em;
            justify-content: center;
        }}
        
        .stDownloadButton button {{
            background: linear-gradient(90deg, {THEME_CONFIG["primary_brand_color"]} 60%, {THEME_CONFIG["secondary_accent_color"]} 100%);
            color: #fff;
            font-weight: 600;
            border-radius: 12px;
            border: none;
            padding: 0.7em 1.5em;
            font-size: 1.08em;
            box-shadow: 0 2px 8px {THEME_CONFIG["primary_brand_color"]}10;
            transition: background 0.18s, color 0.18s;
            margin-bottom: 0.5em;
        }}
        
        .stDownloadButton button:hover {{
            background: linear-gradient(90deg, #005fa3 60%, #009bb0 100%);
            color: #fff;
        }}
        
        /* Skill recommendation cards */
        .skill-card {{
            background: white;
            border-radius: 12px;
            padding: 1em 1.2em;
            margin-bottom: 0.8em;
            border-left: 4px solid {THEME_CONFIG["primary_brand_color"]};
            margin-top: 0.5em;
            box-shadow: 0 2px 8px {THEME_CONFIG["primary_brand_color"]}10;
            border: 1.5px solid #e3e3e3;
        }}
    </style>
    """

def get_section_header(icon: str, title: str) -> str:
    """
    Generate a styled section header.
    
    Args:
        icon: Emoji icon for the section
        title: Title text
        
    Returns:
        HTML string for section header
    """
    return f"""
    <div style='display:flex;align-items:center;gap:0.7em;margin-bottom:0.7em;'>
        <span style='font-size:1.7em;'>{icon}</span>
        <span style='font-size:1.3em;font-weight:700;'>{title}</span>
    </div>
    """

def get_gradient_box(title: str, start_color: str = "#e3f2fd", end_color: str = "#f1f8e9", angle: int = 90) -> str:
    """
    Generate a gradient box for section headers.
    
    Args:
        title: Title text for the box
        start_color: Starting color of gradient
        end_color: Ending color of gradient
        angle: Gradient angle in degrees
        
    Returns:
        HTML string for gradient box
    """
    return f"""
    <div style='background:linear-gradient({angle}deg,{start_color} 60%,{end_color} 100%);border-radius:14px;padding:0.7em 1.1em;margin-bottom:1em;box-shadow:0 2px 12px #0072c610;'>
        {title}
    </div>
    """



def get_professional_legacy_metric_styles() -> str:
    """Get CSS styles for professional legacy metric cards."""
    return f"""
    <style>
    .professional-legacy-metric {{
        background: linear-gradient(90deg, #e3f2fd 60%, #f1f8e9 100%);
        border-radius: 18px;
        box-shadow: 0 4px 18px #0072c610;
        padding: 1.2em 2em 1.2em 1.5em;
        margin-bottom: 1.2em;
        display: flex;
        align-items: center;
        gap: 1.5em;
    }}
    .professional-legacy-metric .score {{
        font-size: 2.5em;
        font-weight: 700;
        color: #0072C6;
        margin-right: 0.5em;
    }}
    .professional-legacy-metric .badge {{
        font-size: 1.25em;
        font-weight: 600;
        padding: 0.3em 1.1em;
        border-radius: 16px;
        background: #fff;
        border: 2px solid #0072C6;
        color: #0072C6;
        margin-left: 1em;
    }}
    .professional-legacy-metric .badge.good {{ background: #e8f5e9; color: #388e3c; border-color: #388e3c;}}
    .professional-legacy-metric .badge.moderate {{ background: #fffde7; color: #fbc02d; border-color: #fbc02d;}}
    .professional-legacy-metric .badge.low {{ background: #ffebee; color: #d32f2f; border-color: #d32f2f;}}
    </style>
    """

def get_radio_button_styles() -> str:
    """Get CSS styles for custom radio buttons."""
    return """
    <style>
    div[data-baseweb="radio"] > div {
        display: flex;
        gap: 1.5em;
        margin-bottom: 1.2em;
    }
    div[data-baseweb="radio"] label {
        background: #f6f8fa;
        border: 2px solid #0072C6;
        border-radius: 20px;
        padding: 0.5em 1.5em;
        font-weight: 600;
        color: #0072C6;
        font-size: 1.08em;
        transition: all 0.18s;
        box-shadow: 0 2px 8px #0072c610;
        margin-bottom: 0;
        cursor: pointer;
        position: relative;
        display: flex;
        align-items: center;
    }
    div[data-baseweb="radio"] input[type="radio"] {
        opacity: 0;
        position: absolute;
    }
    div[data-baseweb="radio"] label:before {
        content: '';
        display: inline-block;
        width: 1.15em;
        height: 1.15em;
        margin-right: 0.7em;
        vertical-align: middle;
        border-radius: 50%;
        border: 2.5px solid #0072C6;
        background: #fff;
        box-shadow: 0 2px 8px #0072c610;
        transition: border-color 0.2s, background 0.2s;
    }
    div[data-baseweb="radio"] input[type="radio"]:checked + div:before {
        background: linear-gradient(90deg, #0072C6 70%, #4CAF50 100%);
        border: 2.5px solid #0072C6;
        box-shadow: 0 4px 16px #0072c620;
    }
    div[data-baseweb="radio"] input[type="radio"]:checked + div {
        background: linear-gradient(90deg, #0072C6 70%, #4CAF50 100%);
        color: #fff !important;
        border: 2px solid #0072C6;
        box-shadow: 0 4px 16px #0072c620;
    }
    </style>
    """

def get_dual_header_styles() -> str:
    """Get CSS styles for dual header sections."""
    return """
    <style>
    .dual-header-row {
        display: flex;
        align-items: center;
        gap: 2em;
        margin-bottom: 0.7em;
        flex-wrap: wrap;
    }
    .dual-header-row > div {
        display: flex;
        align-items: center;
        gap: 0.7em;
        width: 48%;
        justify-content: flex-start;
    }
    .dual-header-badge {
        background: #0072C6;
        color: #fff;
        font-weight: 700;
        border-radius: 50%;
        width: 2.2em;
        height: 2.2em;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3em;
        box-shadow: 0 2px 8px #0072c620;
    }
    .dual-header-title {
        font-size: 1.35em;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .dual-header-title span {
        color: #0072C6;
    }
    @media (max-width: 900px) {
        .dual-header-row { flex-direction: column; gap: 0.2em; }
        .dual-header-row > div { width: 100%; justify-content: flex-start; }
    }
    </style>
    """

def get_expander_content_styles() -> str:
    """Get CSS styles for expander content."""
    return """
    <style>
    .stExpanderContent {
        background: #f9fafd;
        border-radius: 12px;
        padding: 1em 1.2em;
        margin-top: 0.5em;
        box-shadow: 0 2px 8px #0072c610;
        border: 1.5px solid #e3e3e3;
    }
    </style>
    """

def get_download_button_styles() -> str:
    """Get CSS styles for download buttons."""
    return f"""
    <style>
    .download-btn-row {{
        display: flex;
        flex-direction: row;
        gap: 1.1em;
        margin-top: 0.5em;
        margin-bottom: 1.5em;
        justify-content: center;
    }}
    .stDownloadButton button {{
        background: linear-gradient(90deg, #0072C6 60%, #00B8D9 100%);
        color: #fff;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        padding: 0.7em 1.5em;
        font-size: 1.08em;
        box-shadow: 0 2px 8px #0072c610;
        transition: background 0.18s, color 0.18s;
        margin-bottom: 0.5em;
    }}
    .stDownloadButton button:hover {{
        background: linear-gradient(90deg, #005fa3 60%, #009bb0 100%);
        color: #fff;
    }}
    </style>
    """

def get_professional_metric_card_styles() -> str:
    """Get professional metric card styles that match the SmartMatch theme."""
    return f"""
    <style>
    .professional-metric-card {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(25, 118, 210, 0.12);
    }}
    
    .professional-metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(25, 118, 210, 0.25) !important;
    }}
    
    .professional-metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.8) 100%);
        opacity: 0.6;
    }}
    
    .professional-metric-card h3 {{
        font-family: 'Segoe UI', sans-serif;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 1px;
        margin: 0 0 15px 0;
        opacity: 0.9;
        font-weight: 500;
    }}
    
    .professional-metric-card .metric-value {{
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        line-height: 1;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2);
        margin: 12px 0;
    }}
    
    .professional-metric-card .metric-subtitle {{
        font-family: 'Segoe UI', sans-serif;
        font-weight: 400;
        opacity: 0.95;
        letter-spacing: 0.2px;
        margin: 0;
    }}
    
    @media (max-width: 768px) {{
        .professional-metric-card {{
            padding: 20px 15px !important;
        }}
        .professional-metric-card h3 {{
            font-size: 0.8rem;
        }}
        .professional-metric-card .metric-value {{
            font-size: 2.2rem !important;
        }}
        .professional-metric-card .metric-subtitle {{
            font-size: 0.9rem;
        }}
    }}
    </style>
    """

# Professional function aliases for consistent naming
def get_main_application_styles() -> str:
    """Get main application styles for professional UI."""
    return get_main_styles()

def get_metric_card_styles() -> str:
    """Get metric card styles for professional dashboard."""
    return get_professional_metric_card_styles() + get_professional_legacy_metric_styles()

def get_expandable_content_styles() -> str:
    """Get expandable content styles for professional layout."""
    return get_expander_content_styles()
