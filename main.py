import streamlit as st
import pandas as pd

# --- IMPORTS ---
from utils.helpers import scroll_to_top
from utils.styles import inject_css 
from data.loader import load_data, get_empresas_con_contactos, load_entidades

# Vistas
from views.home import show_home
from views.explorer import show_explorer
from views.detail import show_detail
from views.personas import show_personas
from views.entidades import show_entidades

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="Asier Dorronsoro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()
scroll_to_top()

# --- CARGA DE DATOS ---
df_main, df_alumni = load_data()
empresas_alumni = get_empresas_con_contactos(df_alumni)
df_entidades = load_entidades()

# --- INICIALIZACIÓN DE ESTADO ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_empresa' not in st.session_state: st.session_state.selected_empresa = None
if 'current_page' not in st.session_state: st.session_state.current_page = 0
if 'scroll_needed' not in st.session_state: st.session_state.scroll_needed = False

# Filtros Empresas (Valores por defecto)
if 'f_nombre' not in st.session_state: st.session_state.f_nombre = ""
if 'f_provincia' not in st.session_state: st.session_state.f_provincia = []
if 'f_patentes' not in st.session_state: st.session_state.f_patentes = "Todos"
if 'f_pe' not in st.session_state: st.session_state.f_pe = "Todos"
if 'f_ia' not in st.session_state: st.session_state.f_ia = "Todos"
if 'f_deusto' not in st.session_state: st.session_state.f_deusto = "Todos"

# Filtros Personas (Valores por defecto)
if 'f_personas_nombre' not in st.session_state: st.session_state.f_personas_nombre = ""
if 'f_personas_empresa' not in st.session_state: st.session_state.f_personas_empresa = ""
if 'f_personas_provincia' not in st.session_state: st.session_state.f_personas_provincia = []
if 'f_personas_jerarquia' not in st.session_state: st.session_state.f_personas_jerarquia = []
if 'f_personas_funcion' not in st.session_state: st.session_state.f_personas_funcion = ""
if 'current_page_personas' not in st.session_state: st.session_state.current_page_personas = 0

# --- ENRUTADOR DE PÁGINAS ---
if st.session_state.page == 'home':
    show_home()

elif st.session_state.page == 'explorer':
    show_explorer(df_main, df_alumni, empresas_alumni)

elif st.session_state.page == 'detail':
    if st.session_state.selected_empresa:
        show_detail(st.session_state.selected_empresa, df_main, df_alumni)
    else:
        st.session_state.page = 'explorer'
        st.rerun()

elif st.session_state.page == 'personas':
    show_personas(df_main, df_alumni)

elif st.session_state.page == 'entidades':   
    show_entidades(df_entidades)