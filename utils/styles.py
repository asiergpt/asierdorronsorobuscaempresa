# Archivo: utils/styles.py
import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; font-size: 16px; color: #2c3e50; }
    
    /* Títulos */
    .section-title { color: #1F4E79; font-size: 1.8rem; font-weight: 700; margin-top: 2.5rem; border-bottom: 4px solid #DAE9F7; padding-bottom: 5px; margin-bottom: 20px;}

    /* KPIs */
    .kpi-card { background-color: #DAE9F7; border-radius: 12px; padding: 20px; text-align: center; border: 2px solid #1F4E79; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: center; }
    .kpi-value { color: #1F4E79; font-size: 2rem; font-weight: 800; line-height: 1.2; }
    .kpi-label { font-size: 0.85rem; text-transform: uppercase; font-weight: 700; color: #1F4E79; margin-top: 5px; letter-spacing: 1px; }

    /* Tarjetas Tech */
    .tech-hero { background-color: #1F4E79; color: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 10px rgba(31, 78, 121, 0.2); }
    .tech-hero-label { font-size: 0.85rem; text-transform: uppercase; opacity: 0.9; font-weight: 600; margin-bottom: 5px; }
    .tech-hero-val { font-size: 1.3rem; font-weight: 700; }

    .tech-card { background-color: white; border: 1px solid #e0e0e0; border-top: 4px solid #1F4E79; border-radius: 10px; padding: 20px; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s; }
    .tech-card:hover { transform: translateY(-3px); }
    .tech-icon { font-size: 1.8rem; margin-bottom: 10px; display: block; }
    .tech-title { color: #1F4E79; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; text-transform: uppercase; }
    .tech-text { font-size: 1rem; color: #444; line-height: 1.4; }

    /* Tablas */
    .custom-table { width: 100%; border-collapse: separate; border-spacing: 0; min-width: 500px; border-radius: 8px; overflow: hidden; border: 1px solid #eee; }
    .custom-table th { background-color: #1F4E79; color: white; padding: 12px; text-align: center; font-weight: 600; }
    .custom-table td { border-bottom: 1px solid #f0f0f0; padding: 12px; text-align: center; color: #333; }
    .table-container { overflow-x: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.03); border-radius: 8px; margin-bottom: 20px; }

    /* Layouts Grid Puro */
    .responsive-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 20px;
        align-items: stretch;
    }
    
    @media (max-width: 768px) {
        .responsive-grid { grid-template-columns: 1fr; }
        .grid-2, .grid-3 { display: grid; grid-template-columns: 1fr; gap: 15px;}
    }
    
    @media (min-width: 769px) {
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 20px; }
    }

    .box-header { color: #1F4E79; font-weight: 700; font-size: 1.2rem; margin-bottom: 10px; border-bottom: 2px solid #DAE9F7; display: block; }
    
    .content-box { 
        background-color: white; 
        border: 1px solid #dcdcdc; 
        border-radius: 12px; 
        padding: 20px; 
        height: 100%; 
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Home */
    .hero-title { color: #1F4E79; font-size: 4rem; font-weight: 900; text-align: center; margin-bottom: 5px; letter-spacing: -1px; }
    .hero-subtitle { color: #555; font-size: 1.5rem; text-align: center; margin-bottom: 50px; font-weight: 300; }
    .feature-card { background-color: white; border-radius: 12px; padding: 25px; text-align: center; border: 1px solid #eee; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.3s ease; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
    .feature-card:hover { transform: translateY(-5px); border-color: #DAE9F7; }
    .feature-icon { font-size: 3rem; margin-bottom: 15px; display: block; }
    .feature-title { color: #1F4E79; font-weight: 700; font-size: 1.2rem; margin-bottom: 10px; }
    .feature-desc { color: #666; font-size: 1rem; line-height: 1.5; margin-bottom: 20px; }
    
    .results-bar { background-color: #e3f2fd; color: #0d47a1; padding: 12px 20px; border-radius: 8px; font-weight: 500; margin-bottom: 20px; border-left: 5px solid #1F4E79; display: flex; justify-content: space-between; align-items: center; }
    
    /* --- BADGES PROFESIONALES (Diseño Limpio Corporate) --- */
    .badge-top { 
        background-color: #1F4E79;
        color: white; 
        padding: 5px 10px; 
        border-radius: 4px; 
        font-size: 0.85rem; 
        font-weight: 500;
        display: inline-block;
        min-width: 140px;
        text-align: center;
        text-decoration: none !important;
    }
    .badge-mid { 
        background-color: #E3F2FD;
        color: #1565C0; 
        padding: 5px 10px; 
        border-radius: 4px; 
        font-size: 0.85rem; 
        font-weight: 500; 
        display: inline-block;
        min-width: 140px;
        text-align: center;
        text-decoration: none !important;
    }
    .badge-entry { 
        background-color: #F5F5F5;
        color: #616161; 
        padding: 5px 10px; 
        border-radius: 4px; 
        font-size: 0.85rem; 
        font-weight: 500; 
        display: inline-block;
        min-width: 140px;
        text-align: center;
        text-decoration: none !important;
    }
    
    /* Export buttons */
    .export-button-container { margin: 20px 0; }
    
    /* Estilos HOME adicionales */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .hero-section h1 { font-size: 3.5em; font-weight: 800; margin: 0; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); letter-spacing: -1px; }
    .card-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px; }
    .card { background: white; border-radius: 15px; padding: 40px 30px; text-align: center; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1); transition: all 0.3s ease; border-top: 5px solid; cursor: pointer; }
    .card:hover { transform: translateY(-8px); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15); }
    .card-empresas { border-top-color: #667eea; }
    .card-profesionales { border-top-color: #f093fb; }
    .card-icon { font-size: 4em; margin-bottom: 15px; }
    .card h3 { font-size: 1.5em; margin: 15px 0 10px 0; color: #333; font-weight: 700; }
    .card p { font-size: 0.95em; color: #666; margin: 10px 0 0 0; line-height: 1.5; }
    .note-section { background: #f8f9fa; border-left: 5px solid #667eea; padding: 20px 25px; border-radius: 10px; margin-top: 10px; }
    .note-section p { margin: 0; color: #555; font-size: 0.95em; line-height: 1.6; }
    
    @media (max-width: 1024px) {
        .card-container { grid-template-columns: 1fr; }
        .hero-section h1 { font-size: 2.5em; }
    }
    </style>
    """, unsafe_allow_html=True)