import streamlit as st
import pandas as pd
import math
from utils.helpers import (
    clean_number_format, safe_get_val, capitalize_first_letter, 
    render_table
)

ITEMS_PER_PAGE = 20

def get_empresa_name(row):
    """Retorna nombre_matriz_einforma o nombre_dba si no existe"""
    matriz = safe_get_val(row, 'nombre_matriz_einforma', default=None)
    if matriz and matriz != "-":
        return matriz
    return safe_get_val(row, 'nombre_dba', default="-")

def show_personas(df_main, df_alumni):
    st.title("🤝 Buscar Profesionales")
    st.markdown("Encuentra a los profesionales clave en tu base de datos de contactos.")
    
    with st.sidebar:
        st.header("🔍 Filtros de Búsqueda")
        if st.button("⬅️ Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        st.divider()
        
        # Filtro Nombre
        st.session_state.f_personas_nombre = st.text_input("Nombre Persona", value=st.session_state.f_personas_nombre)
        
        # Filtro Empresa
        st.session_state.f_personas_empresa = st.text_input("Empresa", value=st.session_state.f_personas_empresa)

        # Filtro Provincia
        if not df_main.empty:
            provs = sorted(df_main['provincia'].dropna().unique().tolist())
            st.session_state.f_personas_provincia = st.multiselect("Provincia Empresa", provs, default=st.session_state.f_personas_provincia)

        if not df_alumni.empty:
            # Filtro Jerarquía
            jerarquias = sorted([j for j in df_alumni['jerarquía'].dropna().astype(str).str.strip().unique().tolist() if j.lower() not in ['nan', '-', '']])
            st.session_state.f_personas_jerarquia = st.multiselect("Nivel Jerárquico", jerarquias, default=st.session_state.f_personas_jerarquia)
            
            # Filtro Función
            funciones = sorted([f for f in df_alumni['función'].dropna().astype(str).str.strip().unique().tolist() if f.lower() not in ['nan', '-', '']])
            st.session_state.f_personas_funcion = st.multiselect("Función", funciones, default=st.session_state.f_personas_funcion)
        
        st.divider()
        if st.button("🔄 Limpiar Filtros", use_container_width=True):
            st.session_state.f_personas_nombre = ""
            st.session_state.f_personas_empresa = ""
            st.session_state.f_personas_provincia = []
            st.session_state.f_personas_jerarquia = []
            st.session_state.f_personas_funcion = []
            st.session_state.current_page_personas = 0
            st.rerun()

    # --- LÓGICA DE FILTRADO ---
    df_personas = df_alumni.copy() if not df_alumni.empty else pd.DataFrame()
    
    if df_personas.empty:
        st.warning("❌ No hay datos de contactos disponibles.")
        return

    # Helper columna empresa
    df_personas['empresa_filtro'] = df_personas.apply(
        lambda row: (row['nombre_matriz_einforma'] if pd.notna(row['nombre_matriz_einforma']) and str(row['nombre_matriz_einforma']).strip() not in ['', 'nan', '-'] else row['nombre_dba']), axis=1
    )

    if st.session_state.f_personas_nombre:
        df_personas = df_personas[df_personas['Nombre'].astype(str).str.contains(st.session_state.f_personas_nombre, case=False, na=False)]
    
    if st.session_state.f_personas_empresa:
        df_personas = df_personas[df_personas['empresa_filtro'].astype(str).str.contains(st.session_state.f_personas_empresa, case=False, na=False)]
    
    if st.session_state.f_personas_provincia:
        empresas_provincia = df_main[df_main['provincia'].isin(st.session_state.f_personas_provincia)]['Nombre'].tolist()
        df_personas = df_personas[df_personas['empresa_filtro'].isin(empresas_provincia)]
    
    if st.session_state.f_personas_jerarquia:
        df_personas = df_personas[df_personas['jerarquía'].astype(str).str.strip().isin(st.session_state.f_personas_jerarquia)]
    
    if st.session_state.f_personas_funcion:
        df_personas = df_personas[df_personas['función'].astype(str).str.strip().isin(st.session_state.f_personas_funcion)]

    # --- PAGINACIÓN ---
    total_items = len(df_personas)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    
    if st.session_state.current_page_personas >= total_pages: st.session_state.current_page_personas = 0
    if st.session_state.current_page_personas < 0: st.session_state.current_page_personas = 0
    
    start_idx = st.session_state.current_page_personas * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    df_page = df_personas.iloc[start_idx:end_idx]

    st.markdown(f"""<div class="results-bar"><div>🎯 <b>{total_items}</b> profesionales encontrados</div><div style="font-size: 0.9rem;">Página {st.session_state.current_page_personas + 1} de {max(1, total_pages)}</div></div>""", unsafe_allow_html=True)
    
    if not df_page.empty:
        for index, row in df_page.iterrows():
            nombre = capitalize_first_letter(safe_get_val(row, 'Nombre'))
            empresa = get_empresa_name(row)
            provincia = "-"
            jerarquia = safe_get_val(row, 'jerarquía')
            funcion = capitalize_first_letter(safe_get_val(row, 'función'))
            
            if empresa != "-":
                empresa_data = df_main[df_main['Nombre'] == empresa]
                if not empresa_data.empty:
                    provincia = capitalize_first_letter(safe_get_val(empresa_data.iloc[0], 'provincia'))
            
            with st.expander(f"👤 **{nombre}** |  🏢 **{empresa}** |  🛠 {funcion}"):
                df_detalle = pd.DataFrame({
                    "Nombre": [nombre], "Empresa": [empresa],
                    "Provincia": [provincia], "Función": [funcion], "Jerarquía": [jerarquia]
                })
                render_table(df_detalle)
                st.write("")
                if empresa != "-" and empresa in df_main['Nombre'].values:
                    if st.button(f"👁️ Ver perfil de {empresa}", key=f"btn_p_{index}", use_container_width=True):
                        st.session_state.selected_empresa = empresa
                        st.session_state.page = 'detail'
                        st.session_state.scroll_needed = True
                        st.rerun()
        
        st.write("")
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.session_state.current_page_personas > 0:
                if st.button("⬅️ Anterior", use_container_width=True):
                    st.session_state.current_page_personas -= 1
                    st.rerun()
        with col_next:
            if st.session_state.current_page_personas < total_pages - 1:
                if st.button("Siguiente ➡️", use_container_width=True):
                    st.session_state.current_page_personas += 1
                    st.rerun()
    else:
        st.warning("⚠️ No hay profesionales que coincidan con estos filtros.")