import streamlit as st
import pandas as pd
import io
import os
import re

# Importamos funciones auxiliares que necesitamos para limpiar
from utils.helpers import standarize_numero_empleados, has_private_equity, uses_ai

# Intento de importar librería de encriptación
try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

def generate_mock_data():
    """Genera datos de ejemplo si no hay archivos"""
    data_emp = {
        'Nombre': ['Tech Solutions SL', 'Industrias Norte SA', 'Innovación Global', 'Caf', 'Idom'],
        'provincia': ['Gipuzkoa', 'Bizkaia', 'Araba', 'Gipuzkoa', 'Bizkaia'],
        'veredicto_final': ['TOP', 'STANDARD', 'GROWTH', 'TOP', 'TOP'],
        'conclusion_sueldo_80k': ['Es VIABLE', 'DIFICIL', 'Es VIABLE', 'VIABLE', 'VIABLE'],
        'ventas_estimado': [5000000, 12000000, 2500000, 450000000, 300000000],
        'numero_empleados': [45, 120, 25, 3000, 4000],
        'ano_constitucion': [2010, 1995, 2018, 1917, 1957],
        'web_oficial': ['www.techsol.com', 'www.norte.com', 'www.innoglo.com', 'www.caf.net', 'www.idom.com'],
        'actividad_resumen': ['SaaS', 'Manufactura', 'Consultoría IA', 'Ferrocarril', 'Ingeniería'],
        'propiedad_accionistas': ['Fundadores', 'Familia', 'VC Fund', 'Publica', 'Empleados'],
        'private_equity_firmas': ['-', '-', 'Sequoia', '-', '-'],
        'cto_actual': ['Jon Doe', 'Mikel Smith', 'Ana García', 'Txomin Perez', 'Luis M.'],
        'tamano_ing': ['15', '5', '10', '200+', '1000+'],
        'usa_inteligencia_artificial': ['Sí', 'No', 'Sí', 'Sí', 'Sí'],
        'plataforma_cloud': ['AWS', 'On-prem', 'Azure', 'Hybrid', 'AWS'],
        'perfil_txt': ['Python, React', 'Java', 'Python, PyTorch', 'C++', 'Java, .NET'],
        'patentes': [2, 0, 5, 50, 10],
        'SECTOR_NOMBRE': ['Tecnología', 'Industria', 'Consultoría', 'Transporte', 'Ingeniería'],
        'financiacion_publica_detalle': ['Hazitek', 'No', 'CDTI', 'Europea', 'No'],
        'solvencia_txt': ['Alta', 'Media', 'Alta', 'Muy Alta', 'Alta']
    }
    return pd.DataFrame(data_emp)

def validate_and_clean_data(df):
    """Valida y limpia datos cargados"""
    if df.empty:
        return df
    
    if 'patentes' in df.columns:
        df['patentes'] = pd.to_numeric(df['patentes'], errors='coerce').fillna(0).astype(int)
    else:
        df['patentes'] = 0
    
    if 'numero_empleados' in df.columns:
        # Usamos la función que importamos de utils.helpers
        df['numero_empleados'] = df['numero_empleados'].apply(standarize_numero_empleados)
    else:
        df['numero_empleados'] = "0"

    required_cols = {
        'private_equity_firmas': 'Ninguno',
        'usa_inteligencia_artificial': 'NO'
    }
    for col, default in required_cols.items():
        if col not in df.columns:
            df[col] = default
        else:
            df[col] = df[col].fillna(default)
    
    if 'veredicto_final' in df.columns:
        df['veredicto_final'] = df['veredicto_final'].str.replace('TIBURÓN', 'TOP', case=False, regex=False)
    
    df = df.drop_duplicates(subset=['Nombre'], keep='first')
    
    return df

@st.cache_data(ttl=3600)
def load_data():
    """Carga datos desde archivos o genera mock data"""
    df_main = None
    df_alumni = pd.DataFrame()
    
    # Intentar cargar CSVs
    files_to_try = ['euskadi_navarra_dollar.csv']
    for file_name in files_to_try:
        if os.path.exists(file_name):
            try: 
                df_main = pd.read_csv(file_name, sep=';', encoding='utf-8', dtype=str)
                break
            except: 
                try: 
                    df_main = pd.read_csv(file_name, sep=';', encoding='latin-1', dtype=str)
                    break
                except: 
                    try: 
                        df_main = pd.read_csv(file_name, sep=',', encoding='utf-8', dtype=str)
                        break
                    except: 
                        pass
    
    # Intentar cargar encriptado
    file_alumni = 'alumni_seguro.enc'
    if os.path.exists(file_alumni) and "encryption_key" in st.secrets and Fernet:
        try:
            key = st.secrets["encryption_key"]
            cipher_suite = Fernet(key)
            with open(file_alumni, 'rb') as file: 
                encrypted_data = file.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            try: 
                df_alumni = pd.read_csv(io.BytesIO(decrypted_data), sep=';', encoding='utf-8')
            except: 
                df_alumni = pd.read_csv(io.BytesIO(decrypted_data), sep=';', encoding='latin-1')
        except Exception as e:
            st.warning(f"⚠️ No se pudieron cargar datos de contactos encriptados")

    if df_main is None or df_main.empty:
        df_main = generate_mock_data()

    df_main = validate_and_clean_data(df_main)
    
    if not df_alumni.empty:
        df_alumni.columns = [c.strip() for c in df_alumni.columns]
        cols_map = {'funcion': 'función', 'jerarquia': 'jerarquía'}
        df_alumni.rename(columns=cols_map, inplace=True)
        
        c_matriz = next((x for x in df_alumni.columns if 'informa' in x.lower()), 'nombre_matriz_einforma')
        if c_matriz in df_alumni.columns: 
            df_alumni[c_matriz] = df_alumni[c_matriz].astype(str).str.strip()
            
    return df_main, df_alumni

@st.cache_data(ttl=3600)
def get_empresas_con_contactos(df_alumni):
    """Retorna set de empresas que tienen contactos en df_alumni"""
    if df_alumni.empty:
        return set()
    
    empresas_set = set(
        df_alumni['nombre_matriz_einforma'].astype(str).str.strip().unique()
    )
    return empresas_set

# Añade esto AL FINAL de data/loader.py

@st.cache_data(ttl=3600)
def load_entidades():
    """Carga el catálogo de entidades del ecosistema"""
    file_name = 'ecosistema_vasco.csv'  # Ojo, he puesto el nombre de tu nuevo archivo
    df = pd.DataFrame()
    
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name, sep=';', encoding='utf-8')
        except:
            df = pd.read_csv(file_name, sep=';', encoding='latin-1')
            
        # Limpieza básica de nombres de columnas por si acaso
        df.columns = [c.strip() for c in df.columns]
            
    return df