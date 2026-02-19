import pandas as pd
import re
import math
import streamlit as st
import streamlit.components.v1 as components

# --- FORMATEO Y LIMPIEZA ---

def clean_number_format(val):
    """Formatea números con separadores de miles, preservando rangos y símbolos"""
    if pd.isna(val): 
        return "-"
    
    val_str = str(val).strip()

    # 1. Rango (ej: 130-150)
    if re.search(r'\d+[-–]\d+', val_str):
        return val_str
    
    # 2. Símbolos al inicio (>, <, +)
    if re.match(r'^[><+]', val_str):
        return val_str
    
    # 3. Número simple
    try:
        val_limpio = val_str.replace('.', '')
        numero = int(val_limpio)
        return "{:,}".format(numero)
    except ValueError:
        pass 
    
    return val_str

def safe_get_val(row, col, default="-"):
    """Obtiene valor con manejo seguro de columnas faltantes"""
    try:
        if col in row.index and pd.notna(row[col]):
            val = str(row[col]).strip()
            return val if val.lower() != "nan" else default
        return default
    except Exception:
        return default

def capitalize_first_letter(text):
    """Capitaliza la primera letra de cada palabra"""
    text = str(text).strip()
    if not text or text == "-" or text.lower() == "nan": 
        return "-"
    return " ".join([word.capitalize() for word in text.split()])

def standarize_numero_empleados(x):
    """Estandariza el número de empleados"""
    if pd.isna(x):
        return "0"
    
    val_str = str(x).strip()
    val_str = re.sub(r'\s*\(.*?\)', '', val_str).strip()
    
    if any(k in val_str.lower() for k in ['sin datos', 'no disponible', 'desconocido', 'n/a']):
        return "0"

    val_lower = val_str.lower()
    if 'menos de' in val_lower or 'menor que' in val_lower:
        val_str = val_str.lower().replace('menos de', '<').replace('menor que', '<')
    elif 'más de' in val_lower or 'mayor que' in val_lower:
        val_str = val_str.lower().replace('más de', '>').replace('mayor que', '>')

    rango_match = re.search(r'([\d\.]+)\s*[-–]\s*([\d\.]+)', val_str)
    if rango_match:
        start = rango_match.group(1).replace('.', '')
        end = rango_match.group(2).replace('.', '')
        return f"{start}-{end}"

    ineq_match = re.search(r'([><+])\s*([\d\.]+)', val_str)
    if ineq_match:
        symbol = ineq_match.group(1)
        num = ineq_match.group(2).replace('.', '')
        return f"{symbol}{num}"

    num_match = re.search(r'([\d\.]+)', val_str)
    if num_match:
        clean_num = num_match.group(1).replace('.', '')
        return clean_num

    return "0"

# --- LÓGICA DE NEGOCIO ---

def has_private_equity(value):
    if pd.isna(value): 
        return False
    negatives = {'ninguno', 'no identificado', 'sin datos', 'n/a', 'nan', '', '-'}
    return str(value).strip().lower() not in negatives

def uses_ai(value):
    if pd.isna(value): 
        return False
    val_str = str(value).strip().lower()
    yes_values = {'sí', 'si', 'yes', 'verdadero', 'activo'}
    no_values = {'no', 'n', 'false', '0', 'falso', 'inactivo', 'nan', '-', ''}
    
    if val_str in yes_values: return True
    elif val_str in no_values: return False
    else: return 'sí' in val_str or 'yes' in val_str or 'si ' in val_str or ' si' in val_str

def get_hierarchy_order(hierarchy_value):
    if pd.isna(hierarchy_value): return 5
    hierarchy_value = str(hierarchy_value).strip().lower()
    order_map = {'top management': 1, 'middle management': 2, 'entry level/others': 3}
    return order_map.get(hierarchy_value, 5)

# --- UI HELPERS ---

def render_table(df):
    if df.empty: 
        st.caption("Sin datos para mostrar.")
        return
    st.markdown(f'<div class="table-container">{df.to_html(index=False, border=0, classes="custom-table", escape=False)}</div>', unsafe_allow_html=True)

def scroll_to_top():
    if st.session_state.get('scroll_needed', False):
        js = '''<script>
            var body = window.parent.document.querySelector(".main");
            body.scrollTop = 0;
        </script>'''
        components.html(js, height=0)