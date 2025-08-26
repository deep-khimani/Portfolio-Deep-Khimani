from flask import Flask, render_template_string, request, redirect, url_for, flash, send_file
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

# GitHub configuration - replace with your username
GITHUB_USERNAME = "deep-khimani"
GITHUB_API_BASE = "https://api.github.com"

# Updated certifications with actual certificates from your Certificates folder
certifications = [
    {"name": "AI Course", "issuer": "30daysCoding", "year": "2024", "icon": "🤖", "file": "Certificate - AI Course.png"},
    {"name": "Blockchain Technology", "issuer": "30daysCoding", "year": "2024", "icon": "⛓️", "file": "Certificate - Blockchain.png"},
    {"name": "Data Analytics Course", "issuer": "30daysCoding", "year": "2024", "icon": "📊", "file": "Certificate - Data Analytics Course.png"},
    {"name": "Java Development Course", "issuer": "30daysCoding", "year": "2024", "icon": "☕", "file": "Certificate - Java Development Course.png"},
    {"name": "Python Development Course", "issuer": "30daysCoding", "year": "2024", "icon": "🐍", "file": "Certificate - Python Development Course.png"},
    {"name": "Python Basic", "issuer": "HackerRank", "year": "2024", "icon": "🏆", "file": "Hackerrank - Python Basic.png"}
]

def get_github_repos():
    """Fetch ALL repositories from GitHub API and auto-generate project data"""
    try:
        # Fetch all pages of repositories
        all_repos = []
        page = 1
        per_page = 100
        
        while True:
            response = requests.get(
                f"{GITHUB_API_BASE}/users/{GITHUB_USERNAME}/repos",
                params={'page': page, 'per_page': per_page, 'sort': 'updated', 'direction': 'desc'},
                timeout=10
            )
            
            if response.status_code == 200:
                repos = response.json()
                if not repos:  # No more repositories
                    break
                all_repos.extend(repos)
                page += 1
            else:
                print(f"Error fetching repos: {response.status_code}")
                break
        
        projects = []
        
        # Enhanced project mappings for ALL your repositories
        project_mappings = {
            "Mastani.ai-A-RAG-Powered-System-for-Historical-Inquiry": {
                "title": "MASTANI.AI - RAG-Powered Historical Intelligence Engine",
                "description": "Making Pune's History Accessible Through AI with RAG + Google Generative AI + LangChain",
                "novelty": "First-of-its-kind localized historical AI assistant for Pune",
                "tech": ["Python", "LangChain", "Google AI", "RAG", "NLP"],
                "detailed_description": "A revolutionary AI-powered chatbot designed to explore Pune's rich history. Built using advanced RAG (Retrieval-Augmented Generation) technology combined with Google's Generative AI and LangChain framework.",
                "features": ["Real-time historical information retrieval", "PDF document processing", "Natural language understanding", "Cultural heritage preservation"],
                "impact": "Preserving and sharing cultural heritage digitally for future generations"
            },
            "DATALENS-AUTO-EDA": {
                "title": "DATALENS - Intelligent EDA Automation Platform",
                "description": "Democratizing Data Analysis with instant insights from raw CSV files with zero configuration",
                "novelty": "Fully automated EDA pipeline adaptable to any dataset structure",
                "tech": ["Python", "Streamlit", "Pandas", "Plotly"],
                "live_link": "https://datalens-auto-eda.streamlit.app/",
                "detailed_description": "An intelligent platform that democratizes data analysis by providing instant insights from raw CSV files with zero configuration required.",
                "features": ["Zero-code data exploration", "Automated visualization generation", "Statistical analysis", "Interactive dashboards"],
                "impact": "Making data science accessible to everyone, regardless of technical background"
            },
            "Real-Time-Human-Detection-Pose-Estimation-with-Entry-Exit-Counting": {
                "title": "OMNIVISION - Real-Time Human Intelligence System",
                "description": "Advanced Computer Vision for Human Analytics with real-time detection and tracking",
                "novelty": "Multi-person pose estimation with real-time activity classification on edge",
                "tech": ["Python", "OpenCV", "MediaPipe", "Computer Vision"],
                "detailed_description": "A sophisticated computer vision system for real-time human analytics with pose estimation and intelligent counting.",
                "features": ["Real-time pose estimation", "Activity classification", "Entry/exit counting", "Multi-person tracking"],
                "impact": "Enhancing security and analytics capabilities for smart buildings and public spaces"
            },
            "Food-Delivery-ETA-Prediction-Analysis-Visualization-and-Modeling": {
                "title": "DELIVERYAI - Predictive Logistics Optimization Engine",
                "description": "Revolutionizing Delivery Operations with Predictive ML and ensemble models",
                "novelty": "Multi-factor ETA prediction using traffic, weather, and demand patterns",
                "tech": ["Python", "ML", "Data Analytics", "Predictive Modeling"],
                "detailed_description": "A comprehensive machine learning solution for optimizing delivery operations using ensemble models.",
                "features": ["Multi-factor ETA prediction", "Geospatial analysis", "Weather integration", "Demand pattern recognition"],
                "impact": "Reducing delivery costs and improving customer satisfaction through intelligent routing"
            },
            "Real-Time-Fake-News-Detection-with-NLP-and-Ensemble-ML": {
                "title": "TRUTHGUARD - Real-Time Misinformation Detection Engine",
                "description": "Fighting Misinformation with Advanced AI Technology using multi-layer NLP",
                "novelty": "Hybrid ensemble approach combining multiple ML algorithms for max accuracy",
                "tech": ["Python", "NLP", "Ensemble Methods", "Text Classification"],
                "live_link": "https://real-time-fake-news-detection-with-nlp-and-ensemble-ml-bzukeqt.streamlit.app/",
                "detailed_description": "An advanced AI system designed to combat misinformation through sophisticated natural language processing.",
                "features": ["Real-time news verification", "Multi-layer NLP analysis", "Confidence scoring", "Linguistic pattern recognition"],
                "impact": "Contributing to information integrity and helping users identify reliable news sources"
            },
            "Comparative-Analysis-of-ML-Algorithms-for-Speech-Emotion-Recognition-Using-MFCC-Features": {
                "title": "EMOTIONSENSE - Advanced Vocal Emotion Intelligence",
                "description": "Decoding Human Emotions Through Advanced Audio Analysis with MFCC features",
                "novelty": "Comparative ML study revealing optimal algorithms for emotion detection",
                "tech": ["Python", "Audio Processing", "MFCC", "ML Classification"],
                "detailed_description": "A comprehensive research project focused on speech emotion recognition using advanced audio signal processing.",
                "features": ["MFCC feature extraction", "Multi-algorithm comparison", "Audio signal processing", "Emotion classification"],
                "impact": "Advancing emotion recognition for healthcare, education, and human-computer interaction"
            },
            "External-Debt-Analysis": {
                "title": "DEBTINSIGHT - Global External Debt Analysis Platform",
                "description": "Comprehensive Analysis of Global External Debt Patterns and Economic Indicators",
                "novelty": "Multi-dimensional debt analysis across countries and time periods",
                "tech": ["Python", "Data Analytics", "Visualization", "Economic Modeling"],
                "detailed_description": "A comprehensive platform for analyzing global external debt patterns, providing insights into economic stability and debt sustainability across nations.",
                "features": ["Cross-country debt comparison", "Temporal trend analysis", "Economic indicator correlation", "Risk assessment modeling"],
                "impact": "Supporting policy makers and economists in understanding global debt dynamics"
            },
            "Predictive-Analysis-of-Uber": {
                "title": "RIDEPREDICT - Uber Demand Forecasting System",
                "description": "Advanced Predictive Analytics for Ride-Sharing Demand and Pricing Optimization",
                "novelty": "Multi-factor demand prediction using temporal, spatial, and external data",
                "tech": ["Python", "Time Series", "ML", "Geospatial Analysis"],
                "detailed_description": "A sophisticated predictive analytics system for forecasting ride-sharing demand, optimizing pricing strategies, and improving resource allocation.",
                "features": ["Demand forecasting", "Price optimization", "Geospatial analysis", "Temporal pattern recognition"],
                "impact": "Optimizing ride-sharing operations and improving service efficiency"
            }
        }
        
        # Function to auto-generate project info for repositories without explicit mappings
        def auto_generate_project_info(repo):
            """Auto-generate project information based on repository data"""
            name = repo['name']
            description = repo.get('description', '') or f"Innovative project: {name}"
            
            # Determine technology stack based on repository language and name patterns
            tech_stack = []
            language = repo.get('language', '')
            if language:
                tech_stack.append(language)
            
            # Add common technologies based on name patterns
            repo_name_lower = name.lower()
            if any(keyword in repo_name_lower for keyword in ['ml', 'machine-learning', 'ai', 'artificial-intelligence']):
                tech_stack.extend(['Machine Learning', 'AI'])
            if any(keyword in repo_name_lower for keyword in ['web', 'html', 'css', 'js', 'react', 'node']):
                tech_stack.extend(['Web Development', 'Frontend'])
            if any(keyword in repo_name_lower for keyword in ['data', 'analysis', 'visualization']):
                tech_stack.extend(['Data Science', 'Analytics'])
            if any(keyword in repo_name_lower for keyword in ['deep', 'neural', 'cnn', 'rnn']):
                tech_stack.extend(['Deep Learning', 'Neural Networks'])
            if any(keyword in repo_name_lower for keyword in ['nlp', 'text', 'language']):
                tech_stack.extend(['NLP', 'Text Processing'])
            if any(keyword in repo_name_lower for keyword in ['computer-vision', 'cv', 'image', 'opencv']):
                tech_stack.extend(['Computer Vision', 'Image Processing'])
            if any(keyword in repo_name_lower for keyword in ['blockchain', 'crypto', 'ethereum']):
                tech_stack.extend(['Blockchain', 'Cryptocurrency'])
            if any(keyword in repo_name_lower for keyword in ['game', 'unity', 'pygame']):
                tech_stack.extend(['Game Development', 'Gaming'])
            if any(keyword in repo_name_lower for keyword in ['mobile', 'android', 'ios', 'flutter']):
                tech_stack.extend(['Mobile Development', 'Cross-platform'])
            
            # Remove duplicates and ensure we have at least the main language
            tech_stack = list(dict.fromkeys(tech_stack))  # Remove duplicates while preserving order
            if not tech_stack and language:
                tech_stack = [language]
            elif not tech_stack:
                tech_stack = ['Software Development']
            
            # Generate features based on repository
            features = [
                f"Built with {language}" if language else "Cross-platform development",
                "Open source implementation",
                "Documented codebase",
                "Production-ready solution"
            ]
            
            # Generate impact statement
            impact = f"Demonstrating expertise in {', '.join(tech_stack[:2])}"
            if 'ml' in repo_name_lower or 'ai' in repo_name_lower:
                impact += " and advancing artificial intelligence applications"
            elif 'web' in repo_name_lower:
                impact += " and modern web development practices"
            elif 'data' in repo_name_lower:
                impact += " and data-driven decision making"
            
            return {
                "description": description,
                "novelty": f"Innovative approach to {name.replace('-', ' ').replace('_', ' ').title()}",
                "tech": tech_stack,
                "detailed_description": f"A comprehensive project showcasing {', '.join(tech_stack)} capabilities. {description}",
                "features": features,
                "impact": impact
            }
        
        # Priority order for displaying projects (featured projects first)
        priority_order = [
            "Mastani.ai-A-RAG-Powered-System-for-Historical-Inquiry",
            "DATALENS-AUTO-EDA",
            "Real-Time-Fake-News-Detection-with-NLP-and-Ensemble-ML",
            "Real-Time-Human-Detection-Pose-Estimation-with-Entry-Exit-Counting",
            "Food-Delivery-ETA-Prediction-Analysis-Visualization-and-Modeling",
            "Comparative-Analysis-of-ML-Algorithms-for-Speech-Emotion-Recognition-Using-MFCC-Features",
            "External-Debt-Analysis",
            "Predictive-Analysis-of-Uber"
        ]
        
        # Process all repositories (non-fork repositories)
        for repo in all_repos:
            if not repo['fork']:  # Only include non-fork repositories
                repo_name = repo['name']
                
                # Use explicit mapping if available, otherwise auto-generate
                if repo_name in project_mappings:
                    mapping = project_mappings[repo_name]
                else:
                    mapping = auto_generate_project_info(repo)
                
                project = {
                    "id": repo_name.lower().replace('-', '_').replace('.', '_'),
                    "title": mapping.get("title", f"{repo_name.replace('-', ' ').replace('_', ' ').title()}"),
                    "description": mapping["description"],
                    "novelty": mapping["novelty"],
                    "tech": mapping["tech"],
                    "link": repo['html_url'],
                    "detailed_description": mapping["detailed_description"],
                    "features": mapping["features"],
                    "impact": mapping["impact"],
                    "stars": repo.get('stargazers_count', 0),
                    "updated_at": repo.get('updated_at', ''),
                    "priority": priority_order.index(repo_name) if repo_name in priority_order else 999
                }
                
                # Add live link if available in mapping
                if "live_link" in mapping:
                    project["live_link"] = mapping["live_link"]
                
                projects.append(project)
        
        # Sort projects by priority (featured first), then by stars, then by last updated
        projects.sort(key=lambda x: (x['priority'], -x['stars'], x['updated_at']), reverse=False)
        
        print(f"Successfully fetched {len(projects)} repositories")
        return projects
        
    except Exception as e:
        print(f"Error fetching GitHub repos: {e}")
        return get_fallback_projects()

def get_fallback_projects():
    """Fallback projects in case GitHub API fails"""
    return [
        {
            "id": "mastani_ai",
            "title": "MASTANI.AI - RAG-Powered Historical Intelligence Engine",
            "description": "Making Pune's History Accessible Through AI with RAG + Google Generative AI + LangChain",
            "novelty": "First-of-its-kind localized historical AI assistant for Pune",
            "tech": ["Python", "LangChain", "Google AI", "RAG", "NLP"],
            "link": "https://github.com/deep-khimani/Mastani.ai-A-RAG-Powered-System-for-Historical-Inquiry",
            "detailed_description": "A revolutionary AI-powered chatbot designed to explore Pune's rich history.",
            "features": ["Real-time historical information retrieval", "PDF document processing", "Natural language understanding"],
            "impact": "Preserving and sharing cultural heritage digitally for future generations",
            "stars": 0,
            "updated_at": "",
            "priority": 0
        }
    ]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deep Khimani - Data Scientist & ML Engineer</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary-bg: #0B0F1A;
        --secondary-bg: #151B2E;
        --card-bg: rgba(21, 27, 46, 0.8);
        --accent-blue: #00D4FF;
        --accent-purple: #6366F1;
        --accent-gradient: linear-gradient(135deg, #00D4FF 0%, #6366F1 100%);
        --text-primary: #FFFFFF;
        --text-secondary: #B8C4D0;
        --text-muted: #64748B;
        --border-color: rgba(0, 212, 255, 0.1);
        --shadow-glow: 0 0 50px rgba(0, 212, 255, 0.1);
    }
    
    body {
        font-family: 'Inter', sans-serif;
        background: var(--primary-bg);
        color: var(--text-primary);
        overflow-x: hidden;
        line-height: 1.6;
    }
    
    /* Sophisticated Background */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(0, 212, 255, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.03) 0%, transparent 50%),
            linear-gradient(135deg, rgba(0, 212, 255, 0.01) 0%, rgba(99, 102, 241, 0.01) 100%);
        z-index: -1;
    }
    
    /* Navigation */
    nav {
        position: fixed;
        top: 0;
        width: 100%;
        background: rgba(11, 15, 26, 0.95);
        backdrop-filter: blur(20px);
        z-index: 1000;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 2rem;
    }
    
    .logo {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--accent-blue);
        text-decoration: none;
        position: relative;
    }
    
    .logo::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--accent-gradient);
        transition: width 0.3s ease;
    }
    
    .logo:hover::after {
        width: 100%;
    }
    
    .nav-menu {
        display: flex;
        list-style: none;
        gap: 2rem;
    }
    
    .nav-link {
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .nav-link:hover,
    .nav-link.active {
        color: var(--text-primary);
        background: rgba(0, 212, 255, 0.1);
    }
    
    /* Hero Section - Left Aligned */
    .hero {
        min-height: 100vh;
        display: flex;
        align-items: center;
        padding: 0 2rem;
        position: relative;
    }
    
    .hero-container {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        align-items: center;
        width: 100%;
    }
    
    .hero-content {
        opacity: 0;
        animation: fadeInLeft 1s ease-out 0.5s forwards;
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .greeting {
        font-size: 1.5rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
        /* Removed animation - static text now */
    }
    
    .hero h1 {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .hero-description {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-bottom: 2.5rem;
        max-width: 500px;
        line-height: 1.7;
    }
    
    .cta-buttons {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .cta-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem 2rem;
        background: var(--accent-gradient);
        color: white;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 212, 255, 0.3);
    }
    
    .cta-button.secondary {
        background: transparent;
        border: 2px solid var(--accent-blue);
        color: var(--accent-blue);
    }
    
    .cta-button.secondary:hover {
        background: var(--accent-blue);
        color: white;
    }
    
    .hero-visual {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    
    .floating-elements {
        position: relative;
        width: 500px;
        height: 500px;
    }
    
    .floating-card {
        position: absolute;
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-glow);
        transition: all 0.3s ease;
        width: 180px;
        min-height: 140px;
    }
    
    /* Fixed positioning to prevent overlap */
    .floating-card:nth-child(1) {
        top: 5%;
        left: 10%;
        animation: floatUpDown 6s ease-in-out infinite;
    }
    
    .floating-card:nth-child(2) {
        bottom: 5%;
        right: 10%;
        animation: floatUpDown 6s ease-in-out infinite 2s;
    }
    
    .floating-card:nth-child(3) {
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: floatCenter 6s ease-in-out infinite 4s;
    }
    
    @keyframes floatUpDown {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes floatCenter {
        0%, 100% { transform: translate(-50%, -50%) translateY(0px); }
        50% { transform: translate(-50%, -50%) translateY(-20px); }
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .card-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .card-subtitle {
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    
    /* Section Styles */
    section {
        padding: 6rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-title {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 3rem;
        color: var(--text-primary);
        font-weight: 700;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 2px;
    }
    
    /* Projects Grid */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .project-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.03), transparent);
        transition: left 0.5s ease;
    }
    
    .project-card:hover::before {
        left: 100%;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 212, 255, 0.3);
        box-shadow: var(--shadow-glow);
    }
    
    .project-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--text-primary);
        line-height: 1.3;
    }
    
    .project-description {
        margin-bottom: 1rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    .project-novelty {
        background: rgba(0, 212, 255, 0.1);
        border-left: 3px solid var(--accent-blue);
        padding: 1rem;
        margin: 1.5rem 0;
        border-radius: 0 8px 8px 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-style: italic;
    }
    
    .project-stats {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    
    .project-stats .stat {
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1.5rem 0;
    }
    
    .tech-tag {
        background: rgba(99, 102, 241, 0.1);
        color: var(--accent-purple);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .project-links {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .github-link, .live-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-primary);
        text-decoration: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        flex: 1;
        min-width: 140px;
        justify-content: center;
    }
    
    .github-link {
        background: var(--accent-gradient);
    }
    
    .live-link {
        background: rgba(34, 197, 94, 0.2);
        border: 2px solid #22c55e;
        color: #22c55e;
    }
    
    .github-link:hover {
        transform: translateX(3px);
        box-shadow: 0 5px 20px rgba(0, 212, 255, 0.2);
    }
    
    .live-link:hover {
        background: #22c55e;
        color: white;
        transform: translateX(3px);
    }
    
    /* Show More Button */
    .show-more-container {
        text-align: center;
        margin-top: 2rem;
    }
    
    .show-more-btn {
        background: var(--accent-gradient);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .show-more-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }
    
    /* Modal Styles */
    .modal {
        display: none;
        position: fixed;
        z-index: 2000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
    }
    
    .modal-content {
        background: var(--secondary-bg);
        margin: 3% auto;
        padding: 3rem;
        border-radius: 20px;
        width: 90%;
        max-width: 800px;
        max-height: 85vh;
        overflow-y: auto;
        border: 1px solid var(--border-color);
        position: relative;
    }
    
    .close {
        position: absolute;
        right: 2rem;
        top: 2rem;
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.3s ease;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .close:hover {
        color: var(--text-primary);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .modal-title {
        font-size: 1.8rem;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .modal-description {
        font-size: 1rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        line-height: 1.7;
    }
    
    .modal-section {
        margin-bottom: 2rem;
    }
    
    .modal-section h3 {
        color: var(--accent-blue);
        font-size: 1.2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .features-list {
        list-style: none;
        padding: 0;
        display: grid;
        gap: 0.8rem;
    }
    
    .features-list li {
        background: rgba(0, 212, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid var(--accent-blue);
        position: relative;
        padding-left: 3rem;
    }
    
    .features-list li::before {
        content: '✓';
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--accent-blue);
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .impact-text {
        background: rgba(99, 102, 241, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 3px solid var(--accent-purple);
        color: var(--text-secondary);
        font-style: italic;
        line-height: 1.6;
    }
    
    /* Certifications Grid */
    .certifications-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .cert-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .cert-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 212, 255, 0.3);
        box-shadow: var(--shadow-glow);
    }
    
    .cert-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .cert-name {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .cert-issuer {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    /* Certificate Modal */
    .cert-modal {
        display: none;
        position: fixed;
        z-index: 2000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(10px);
    }
    
    .cert-modal-content {
        position: relative;
        margin: 2% auto;
        width: 90%;
        max-width: 800px;
        text-align: center;
    }
    
    .cert-modal img {
        width: 100%;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 20px 60px rgba(0, 212, 255, 0.3);
    }
    
    .cert-close {
        position: absolute;
        top: 20px;
        right: 35px;
        color: #f1f1f1;
        font-size: 40px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.3s;
    }
    
    .cert-close:hover {
        color: var(--accent-blue);
    }
    
    /* Contact Section */
    .contact-section {
        background: var(--secondary-bg);
        border-radius: 20px;
        padding: 4rem;
        margin-top: 3rem;
        border: 1px solid var(--border-color);
    }
    
    .contact-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        align-items: start;
    }
    
    .contact-info h3 {
        font-size: 1.5rem;
        color: var(--text-primary);
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    .contact-links {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .contact-link {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: var(--text-secondary);
        text-decoration: none;
        padding: 1rem;
        border-radius: 12px;
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .contact-link:hover {
        color: var(--text-primary);
        background: rgba(0, 212, 255, 0.1);
        border-color: rgba(0, 212, 255, 0.3);
        transform: translateX(5px);
    }
    
    .contact-icon {
        font-size: 1.2rem;
        color: var(--accent-blue);
        width: 20px;
        text-align: center;
    }
    
    .contact-form {
        background: rgba(0, 212, 255, 0.02);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(0, 212, 255, 0.1);
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-group input,
    .form-group textarea {
        width: 100%;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .form-group input:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: var(--accent-blue);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .form-group input::placeholder,
    .form-group textarea::placeholder {
        color: var(--text-muted);
    }
    
    .submit-btn {
        width: 100%;
        padding: 1rem;
        background: var(--accent-gradient);
        border: none;
        border-radius: 8px;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .submit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }
    
    /* Flash Messages */
    .flash-messages {
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 1001;
        max-width: 350px;
    }
    
    .flash-message {
        background: rgba(0, 212, 255, 0.9);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-weight: 500;
        animation: slideInRight 0.5s ease-out;
        box-shadow: 0 5px 25px rgba(0, 212, 255, 0.3);
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100%); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .flash-message.error {
        background: rgba(239, 68, 68, 0.9);
        box-shadow: 0 5px 25px rgba(239, 68, 68, 0.3);
    }
    
    /* Footer */
    footer {
        background: var(--secondary-bg);
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-top: 1px solid var(--border-color);
        color: var(--text-muted);
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
        .hero-container {
            grid-template-columns: 1fr;
            text-align: center;
            gap: 2rem;
        }
        
        .hero-visual {
            order: -1;
        }
        
        .floating-elements {
            width: 300px;
            height: 300px;
        }
        
        .contact-grid {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .nav-container {
            padding: 0 1rem;
        }
        
        .nav-menu {
            gap: 1rem;
        }
        
        .nav-link {
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }
        
        .hero {
            padding: 0 1rem;
        }
        
        .hero h1 {
            font-size: 2.5rem;
        }
        
        .greeting {
            font-size: 1.2rem;
        }
        
        .cta-buttons {
            flex-direction: column;
            align-items: stretch;
        }
        
        .projects-grid {
            grid-template-columns: 1fr;
        }
        
        .certifications-grid {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .project-links {
            flex-direction: column;
        }
        
        section {
            padding: 4rem 1rem;
        }
        
        .project-card,
        .contact-section {
            padding: 2rem;
        }
        
        .modal-content {
            margin: 5% auto;
            padding: 2rem;
            width: 95%;
        }
        
        .floating-elements {
            display: none;
        }
    }
    
    /* Scroll animations */
    .fade-in {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease-out;
    }
    
    .fade-in.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Hidden projects initially */
    .project-card.hidden {
        display: none;
    }
    
    /* Loading animation for GitHub links */
    .github-link.loading::after {
        content: '';
        width: 12px;
        height: 12px;
        border: 2px solid transparent;
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-left: 0.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <a href="#home" class="logo">Deep Khimani</a>
            <ul class="nav-menu">
                <li><a href="#home" class="nav-link active">Home</a></li>
                <li><a href="#projects" class="nav-link">Projects</a></li>
                <li><a href="#certifications" class="nav-link">Certifications</a></li>
                <li><a href="#contact" class="nav-link">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Flash Messages -->
    <div class="flash-messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message {{ 'error' if category == 'error' else '' }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- Project Modal -->
    <div id="projectModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2 id="modalTitle" class="modal-title"></h2>
            <p id="modalDescription" class="modal-description"></p>
            
            <div class="modal-section">
                <h3>Key Features</h3>
                <ul id="modalFeatures" class="features-list"></ul>
            </div>
            
            <div class="modal-section">
                <h3>Technology Stack</h3>
                <div id="modalTech" class="tech-stack"></div>
            </div>
            
            <div class="modal-section">
                <h3>Impact</h3>
                <p id="modalImpact" class="impact-text"></p>
            </div>
            
            <div class="modal-section">
                <div class="project-links">
                    <a id="modalGithub" href="#" class="github-link" target="_blank" rel="noopener noreferrer">
                        <i class="fab fa-github"></i> View on GitHub
                    </a>
                    <a id="modalLiveLink" href="#" class="live-link" target="_blank" rel="noopener noreferrer" style="display: none;">
                        <i class="fas fa-external-link-alt"></i> Live Demo
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Certificate Modal -->
    <div id="certModal" class="cert-modal">
        <span class="cert-close">&times;</span>
        <div class="cert-modal-content">
            <img id="certImage" src="" alt="Certificate">
        </div>
    </div>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <p class="greeting">Hi, I'm</p>
                <h1>Deep Khimani</h1>
                <p class="hero-subtitle">Data Scientist & ML Engineer</p>
                <p class="hero-description">
                    Transforming complex data into intelligent solutions through cutting-edge machine learning, 
                    advanced analytics, and AI-driven innovation that drives meaningful business impact.
                </p>
                <div class="cta-buttons">
                    <a href="#projects" class="cta-button">
                        <i class="fas fa-rocket"></i> View Projects
                    </a>
                    <a href="#contact" class="cta-button secondary">
                        <i class="fas fa-paper-plane"></i> Get In Touch
                    </a>
                </div>
            </div>
            
            <div class="hero-visual">
                <div class="floating-elements">
                    <div class="floating-card">
                        <div class="card-icon">🤖</div>
                        <div class="card-title">Machine Learning</div>
                        <div class="card-subtitle">Advanced AI Models</div>
                    </div>
                    <div class="floating-card">
                        <div class="card-icon">📊</div>
                        <div class="card-title">Data Analytics</div>
                        <div class="card-subtitle">Insights & Visualization</div>
                    </div>
                    <div class="floating-card">
                        <div class="card-icon">🔬</div>
                        <div class="card-title">Research</div>
                        <div class="card-subtitle">Innovation & Discovery</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="fade-in">
        <h2 class="section-title">All Projects ({{ projects|length }} Repositories)</h2>
        <div class="projects-grid" id="projectsGrid">
            {% for project in projects %}
            <div class="project-card {% if loop.index > 6 %}hidden{% endif %}" onclick="openProjectModal('{{ project.id }}')" data-index="{{ loop.index }}">
                <h3 class="project-title">{{ project.title }}</h3>
                <p class="project-description">{{ project.description }}</p>
                
                <div class="project-novelty">
                    <strong>Innovation:</strong> {{ project.novelty }}
                </div>
                
                {% if project.stars > 0 %}
                <div class="project-stats">
                    <div class="stat">
                        <i class="fas fa-star"></i>
                        <span>{{ project.stars }}</span>
                    </div>
                </div>
                {% endif %}
                
                <div class="tech-stack">
                    {% for tech in project.tech %}
                    <span class="tech-tag">{{ tech }}</span>
                    {% endfor %}
                </div>
                
                <div class="project-links">
                    <a href="{{ project.link }}" class="github-link" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();">
                        <i class="fab fa-github"></i> Repository
                    </a>
                    {% if project.live_link %}
                    <a href="{{ project.live_link }}" class="live-link" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();">
                        <i class="fas fa-external-link-alt"></i> Live Demo
                    </a>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        
        {% if projects|length > 6 %}
        <div class="show-more-container">
            <button class="show-more-btn" id="showMoreBtn" onclick="showMoreProjects()">
                <i class="fas fa-chevron-down"></i> Show More Projects ({{ projects|length - 6 }} remaining)
            </button>
        </div>
        {% endif %}
    </section>

    <!-- Certifications Section -->
    <section id="certifications" class="fade-in">
        <h2 class="section-title">Certifications & Expertise</h2>
        <div class="certifications-grid">
            {% for cert in certifications %}
            <div class="cert-card" onclick="openCertModal('{{ cert.file }}')">
                <div class="cert-icon">{{ cert.icon }}</div>
                <h3 class="cert-name">{{ cert.name }}</h3>
                <p class="cert-issuer">{{ cert.issuer }} • {{ cert.year }}</p>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="fade-in">
        <h2 class="section-title">Let's Connect</h2>
        <div class="contact-section">
            <div class="contact-grid">
                <div class="contact-info">
                    <h3>Get In Touch</h3>
                    <div class="contact-links">
                        <a href="https://github.com/deep-khimani" class="contact-link" target="_blank" rel="noopener noreferrer">
                            <div class="contact-icon">
                                <i class="fab fa-github"></i>
                            </div>
                            <div>
                                <div>GitHub</div>
                                <small>@deep-khimani</small>
                            </div>
                        </a>
                        
                        <a href="https://www.linkedin.com/in/deep-khimani-91bb1b24a/" class="contact-link" target="_blank" rel="noopener noreferrer">
                            <div class="contact-icon">
                                <i class="fab fa-linkedin"></i>
                            </div>
                            <div>
                                <div>LinkedIn</div>
                                <small>Professional Network</small>
                            </div>
                        </a>
                        
                        <a href="mailto:deep.khimani.btech2022@sitpune.edu.in" class="contact-link">
                            <div class="contact-icon">
                                <i class="fas fa-envelope"></i>
                            </div>
                            <div>
                                <div>Email</div>
                                <small>deep.khimani.btech2022@sitpune.edu.in</small>
                            </div>
                        </a>
                        
                        <a href="tel:+917069833874" class="contact-link">
                            <div class="contact-icon">
                                <i class="fas fa-phone"></i>
                            </div>
                            <div>
                                <div>Phone</div>
                                <small>+91 70698 33874</small>
                            </div>
                        </a>
                    </div>
                </div>
                
                <form method="POST" action="/contact" class="contact-form">
                    <div class="form-group">
                        <input type="text" name="name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" name="email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <input type="text" name="subject" placeholder="Subject" required>
                    </div>
                    <div class="form-group">
                        <textarea name="message" rows="5" placeholder="Your Message" required></textarea>
                    </div>
                    <button type="submit" class="submit-btn">
                        <i class="fas fa-paper-plane"></i> Send Message
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <p>&copy; 2025 Deep Khimani. All rights reserved. | Crafting intelligent solutions with data and AI.</p>
    </footer>

    <script>
        // Project data for modal
        const projectData = {
            {% for project in projects %}
            '{{ project.id }}': {
                title: '{{ project.title }}',
                description: '{{ project.detailed_description }}',
                features: {{ project.features | tojson }},
                tech: {{ project.tech | tojson }},
                impact: '{{ project.impact }}',
                link: '{{ project.link }}',
                liveLink: {{ project.live_link | tojson if project.live_link else 'null' }}
            },
            {% endfor %}
        };
        
        // Show more projects functionality
        let currentlyShown = 6;
        const totalProjects = {{ projects|length }};
        
        function showMoreProjects() {
            const hiddenProjects = document.querySelectorAll('.project-card.hidden');
            const projectsToShow = Math.min(6, hiddenProjects.length);
            
            for (let i = 0; i < projectsToShow; i++) {
                hiddenProjects[i].classList.remove('hidden');
            }
            
            currentlyShown += projectsToShow;
            
            const showMoreBtn = document.getElementById('showMoreBtn');
            const remaining = totalProjects - currentlyShown;
            
            if (remaining > 0) {
                showMoreBtn.innerHTML = `<i class="fas fa-chevron-down"></i> Show More Projects (${remaining} remaining)`;
            } else {
                showMoreBtn.style.display = 'none';
            }
        }
        
        // Modal functionality
        function openProjectModal(projectId) {
            const project = projectData[projectId];
            const modal = document.getElementById('projectModal');
            
            document.getElementById('modalTitle').textContent = project.title;
            document.getElementById('modalDescription').textContent = project.description;
            document.getElementById('modalImpact').textContent = project.impact;
            document.getElementById('modalGithub').href = project.link;
            
            // Handle live link
            const liveLink = document.getElementById('modalLiveLink');
            if (project.liveLink) {
                liveLink.href = project.liveLink;
                liveLink.style.display = 'inline-flex';
            } else {
                liveLink.style.display = 'none';
            }
            
            // Populate features
            const featuresList = document.getElementById('modalFeatures');
            featuresList.innerHTML = '';
            project.features.forEach(feature => {
                const li = document.createElement('li');
                li.textContent = feature;
                featuresList.appendChild(li);
            });
            
            // Populate tech stack
            const techDiv = document.getElementById('modalTech');
            techDiv.innerHTML = '';
            project.tech.forEach(tech => {
                const span = document.createElement('span');
                span.className = 'tech-tag';
                span.textContent = tech;
                techDiv.appendChild(span);
            });
            
            modal.style.display = 'block';
        }
        
        // Certificate modal functionality
        function openCertModal(filename) {
            const modal = document.getElementById('certModal');
            const img = document.getElementById('certImage');
            img.src = `/certificates/${filename}`;
            img.alt = filename;
            modal.style.display = 'block';
        }
        
        // Close modals
        document.querySelector('.close').onclick = function() {
            document.getElementById('projectModal').style.display = 'none';
        }
        
        document.querySelector('.cert-close').onclick = function() {
            document.getElementById('certModal').style.display = 'none';
        }
        
        window.onclick = function(event) {
            const projectModal = document.getElementById('projectModal');
            const certModal = document.getElementById('certModal');
            if (event.target == projectModal) {
                projectModal.style.display = 'none';
            }
            if (event.target == certModal) {
                certModal.style.display = 'none';
            }
        }

        // Smooth scrolling and active nav
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Active navigation highlighting
        window.addEventListener('scroll', function() {
            const sections = document.querySelectorAll('section');
            const navLinks = document.querySelectorAll('.nav-link');
            
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (scrollY >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });

        // Scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });

        // Auto-hide flash messages
        setTimeout(function() {
            const flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(message => {
                message.style.animation = 'slideInRight 0.5s ease-out reverse';
                setTimeout(() => message.remove(), 500);
            });
        }, 5000);
    </script>
</body>
</html>
'''

def send_email(name, email, subject, message):
    """Send email notification when someone contacts via the form"""
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"  # Replace with your sending email  
        sender_password = "your-app-password"  # Replace with your app password
        receiver_email = "deep.khimani.btech2022@sitpune.edu.in"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Portfolio Contact: {subject}"
        
        # Email body
        body = f"""
        New contact form submission from your portfolio:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        
        ---
        Sent via Portfolio Contact Form
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route('/')
def home():
    # Fetch ALL projects dynamically from GitHub
    projects = get_github_repos()
    return render_template_string(HTML_TEMPLATE, projects=projects, certifications=certifications)

@app.route('/certificates/<filename>')
def serve_certificate(filename):
    """Serve certificate images from Certificates folder"""
    try:
        # Look for certificates in multiple possible locations
        possible_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Certificates', filename),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certificates', filename),
            os.path.join('Certificates', filename),
            os.path.join('certificates', filename),
            filename  # If it's in the same directory
        ]
        
        for cert_path in possible_paths:
            if os.path.exists(cert_path):
                return send_file(cert_path)
        
        # If no certificate found, return 404
        from flask import abort
        abort(404)
        
    except Exception as e:
        print(f"Error serving certificate: {e}")
        from flask import abort
        abort(404)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Send email notification
        if send_email(name, email, subject, message):
            flash('Message sent successfully! Thank you for reaching out. I will get back to you soon!', 'success')
        else:
            # Still show success to user, but log the email failure
            flash('Message received! I will get back to you soon!', 'success')
            print(f"Contact form submission (email failed): {name} ({email}) - {subject}: {message}")
        
    except Exception as e:
        flash('Failed to send message. Please try again later.', 'error')
        print(f"Contact form error: {e}")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
