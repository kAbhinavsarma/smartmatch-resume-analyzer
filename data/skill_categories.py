"""
Professional Skill Categories and Learning Resources

This module contains comprehensive skill categorization data used for resume
analysis and skill matching algorithms. Provides structured skill categories,
professional development resources, and utility functions for skill management.

Categories:
    - Programming Languages: Core programming languages and scripting
    - Web Development: Frontend and backend frameworks and libraries  
    - Data Science: Libraries and tools for data analysis and machine learning
    - Infrastructure: Cloud platforms, databases, and deployment tools
    - Business Intelligence: Analytics and visualization platforms
    - Professional Skills: Soft skills and domain expertise

Functions:
    get_skill_category: Retrieve category for a given skill
    get_all_professional_skills: Get comprehensive list of all categorized skills
    get_skills_by_category: Get skills filtered by specific category

Author: Resume Analysis Team
Version: 1.0.0
"""
from typing import List, Set, Dict, Any

# Comprehensive skill categories for professional assessment
PROFESSIONAL_SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "c++", "c", "c#", "go", "typescript", "javascript", "sql", 
        "r", "bash", "html", "css", "kotlin", "swift", "dart", "rust", "scala", "php"
    ],
    "Data Science Libraries": [
        "numpy", "pandas", "matplotlib", "seaborn", "plotly", "scikit-learn", "xgboost",
        "lightgbm", "catboost", "tensorflow", "keras", "pytorch", "statsmodels", 
        "opencv", "nltk", "spacy", "transformers", "gensim", "dask", "polars"
    ],
    "Web Development Frameworks": [
        "flask", "django", "fastapi", "express", "next.js", "nuxt.js", "spring boot", 
        "ruby on rails", "laravel", "svelte", "vue.js", "react", "angular", "blazor"
    ],
    "Development Tools": [
        "git", "github", "gitlab", "bitbucket", "docker", "kubernetes", "jenkins", 
        "ansible", "vagrant", "jira", "postman", "powershell", "linux", "terminal", 
        "notion", "slack", "vs code", "pycharm", "eclipse", "intellij", "android studio"
    ],
    "Business Intelligence": [
        "excel", "powerbi", "tableau", "looker", "metabase", "qlikview", "superset", 
        "google data studio", "databricks", "alteryx", "domo"
    ],
    "Database Technologies": [
        "mysql", "postgresql", "sqlite", "mongodb", "redis", "cassandra", "neo4j",
        "oracle", "dynamodb", "bigquery", "snowflake", "clickhouse", "elasticsearch"
    ],
    "Cloud Platforms": [
        "aws", "azure", "gcp", "heroku", "vercel", "netlify", "firebase", "supabase", 
        "digitalocean", "linode", "cloudflare"
    ],
    "Big Data Technologies": [
        "hadoop", "spark", "hive", "pig", "kafka", "flink", "sqoop", "airflow", "dbt",
        "databricks", "presto", "trino"
    ],
    "Machine Learning Concepts": [
        "machine learning", "deep learning", "supervised learning", "unsupervised learning",
        "reinforcement learning", "model evaluation", "cross validation", 
        "feature engineering", "model deployment", "dimensionality reduction",
        "ensemble methods", "automl", "hyperparameter tuning"
    ],
    "Artificial Intelligence Domains": [
        "natural language processing", "computer vision", "optical character recognition", 
        "speech recognition", "large language models", "recommendation systems", 
        "chatbots", "generative ai", "prompt engineering"
    ],
    "MLOps and Model Management": [
        "mlflow", "tensorboard", "data version control", "sagemaker", "tfx", "onnx", 
        "torchserve", "gradio", "streamlit", "kubeflow", "feast"
    ],
    "Professional Skills": [
        "project management", "team leadership", "communication", "problem solving",
        "analytical thinking", "stakeholder management", "agile methodology", "scrum"
    ]
}

# Create optimized skill-to-category mapping for efficient lookups
SKILL_TO_CATEGORY_MAPPING = {}
for category, skills in PROFESSIONAL_SKILL_CATEGORIES.items():
    for skill in skills:
        SKILL_TO_CATEGORY_MAPPING[skill.lower()] = category

PROFESSIONAL_SKILL_RECOMMENDATIONS = {
    "python": {
        "description": "High-level programming language essential for data science, web development, and automation. Offers excellent career opportunities across multiple domains.",
        "learning_resource": "https://www.python.org/about/gettingstarted/",
        "priority": "High"
    },
    "machine learning": {
        "description": "Critical field of artificial intelligence enabling systems to learn from data without explicit programming. Essential for modern data science and AI roles.",
        "learning_resource": "https://www.coursera.org/learn/machine-learning",
        "priority": "High"
    },
    "sql": {
        "description": "Standard language for managing and querying relational databases. Fundamental skill for data analysis, backend development, and business intelligence.",
        "learning_resource": "https://www.w3schools.com/sql/",
        "priority": "High"
    },
    "pandas": {
        "description": "Essential Python library for data manipulation and analysis. Critical for data cleaning, transformation, and exploratory data analysis workflows.",
        "learning_resource": "https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html",
        "priority": "High"
    },
    "tensorflow": {
        "description": "Industry-standard open-source machine learning framework by Google. Essential for deep learning and neural network development projects.",
        "learning_resource": "https://www.tensorflow.org/learn",
        "priority": "Medium"
    },
    "docker": {
        "description": "Containerization platform essential for modern DevOps practices. Critical for application deployment, scalability, and development environment consistency.",
        "learning_resource": "https://docs.docker.com/get-started/",
        "priority": "High"
    },
    "react": {
        "description": "Leading JavaScript library for building user interfaces. Highly demanded for frontend web development with component-based architecture.",
        "learning_resource": "https://react.dev/learn",
        "priority": "High"
    },
    "aws": {
        "description": "Amazon Web Services - leading cloud computing platform. Essential for scalable application deployment, data storage, and modern infrastructure management.",
        "learning_resource": "https://aws.amazon.com/getting-started/",
        "priority": "High"
    },
    "tableau": {
        "description": "Industry-leading data visualization tool for creating interactive dashboards and reports. Essential for business intelligence and data analytics roles.",
        "learning_resource": "https://www.tableau.com/learn",
        "priority": "Medium"
    },
    "git": {
        "description": "Version control system fundamental for collaborative software development. Essential for tracking changes, managing code repositories, and team workflows.",
        "learning_resource": "https://git-scm.com/docs/gittutorial",
        "priority": "High"
    },
    "scikit-learn": {
        "description": "Comprehensive Python library for machine learning with efficient tools for data mining and analysis. Essential for practical ML implementation.",
        "learning_resource": "https://scikit-learn.org/stable/getting_started.html",
        "priority": "Medium"
    },
    "javascript": {
        "description": "Versatile programming language for web development, both frontend and backend. Essential for modern web applications and full-stack development.",
        "learning_resource": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
        "priority": "High"
    },
    "numpy": {
        "description": "Fundamental Python library for numerical computing with support for large arrays and mathematical functions. Foundation for data science workflows.",
        "learning_resource": "https://numpy.org/doc/stable/user/quickstart.html",
        "priority": "Medium"
    },
    "communication": {
        "description": "Essential professional skill for explaining technical concepts, collaborating with teams, and presenting findings to stakeholders effectively.",
        "learning_resource": "https://www.coursera.org/learn/communication-skills",
        "priority": "High"
    },
    "deep learning": {
        "description": "Advanced subset of machine learning using neural networks with multiple layers. Essential for AI applications including NLP and computer vision.",
        "learning_resource": "https://www.deeplearning.ai/",
        "priority": "Medium"
    }
}


def get_skill_category(skill_name: str) -> str:
    """
    Retrieve the professional category for a given skill.
    
    Args:
        skill_name: Name of the skill to categorize
        
    Returns:
        Category name or 'Specialized Skills' if not found
    """
    return SKILL_TO_CATEGORY_MAPPING.get(skill_name.lower(), "Specialized Skills")


def get_all_professional_skills() -> Set[str]:
    """
    Return a comprehensive set of all skills across all categories.
    
    Returns:
        Set containing all categorized professional skills
    """
    all_skills = set()
    for skills in PROFESSIONAL_SKILL_CATEGORIES.values():
        all_skills.update(skills)
    return all_skills


def get_skills_by_category(category: str) -> List[str]:
    """
    Get skills filtered by a specific professional category.
    
    Args:
        category: Name of the skill category
        
    Returns:
        List of skills in the specified category
    """
    return PROFESSIONAL_SKILL_CATEGORIES.get(category, [])


def get_skill_recommendation(skill_name: str) -> Dict[str, Any]:
    """
    Get professional development recommendation for a specific skill.
    
    Args:
        skill_name: Name of the skill
        
    Returns:
        Dictionary containing description, learning resource, and priority
    """
    return PROFESSIONAL_SKILL_RECOMMENDATIONS.get(
        skill_name.lower(), 
        {
            "description": "Professional skill requiring development",
            "learning_resource": "https://www.coursera.org/",
            "priority": "Medium"
        }
    )


