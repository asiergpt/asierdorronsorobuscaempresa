import streamlit as st
import pandas as pd
import math
import re
from utils.helpers import (
    clean_number_format, safe_get_val, capitalize_first_letter, 
    has_private_equity, uses_ai
)

ITEMS_PER_PAGE = 20

def show_explorer(df_main, df_alumni, empresas_alumni_set):
    st.title("🚀 Explorador de Empresas")
    st.markdown("Usa los filtros del menú lateral para encontrar tu cliente ideal.")
    
    # --- SIDEBAR FILTROS ---
    with st.sidebar:
        st.header("🔍 Filtros de Búsqueda")
        if st.button("⬅️ Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        st.divider()
        
        st.session_state.f_nombre = st.text_input("Nombre Empresa", value=st.session_state.f_nombre)
        
        provs = sorted(df_main['provincia'].dropna().unique().tolist())
        st.session_state.f_provincia = st.multiselect("Provincia", provs, default=st.session_state.f_provincia)
        
        st.session_state.f_patentes = st.radio("¿Tiene Patentes?", ["Todos", "Sí", "No"], 
                                                index=["Todos", "Sí", "No"].index(st.session_state.f_patentes),
                                                horizontal=True)
        
        st.session_state.f_pe = st.radio("¿Tiene Private Equity?", ["Todos", "Sí", "No"], 
                                          index=["Todos", "Sí", "No"].index(st.session_state.f_pe),
                                          horizontal=True)
        
        st.session_state.f_ia = st.radio("¿Usa Inteligencia Artificial?", ["Todos", "Sí", "No"], 
                                          index=["Todos", "Sí", "No"].index(st.session_state.f_ia),
                                          horizontal=True)
        
        st.session_state.f_deusto = st.radio("¿Deusto Alumni?", ["Todos", "Sí", "No"], 
                                              index=["Todos", "Sí", "No"].index(st.session_state.f_deusto),
                                              horizontal=True)

    # --- LÓGICA DE FILTRADO ---
    df_show = df_main.copy()

    if st.session_state.f_nombre:
        df_show = df_show[df_show['Nombre'].astype(str).str.contains(
            st.session_state.f_nombre, case=False, na=False)]

    if st.session_state.f_provincia:
        df_show = df_show[df_show['provincia'].isin(st.session_state.f_provincia)]

    if st.session_state.f_patentes == "Sí":
        df_show = df_show[df_show['patentes'] > 0]
    elif st.session_state.f_patentes == "No":
        df_show = df_show[df_show['patentes'] == 0]

    if st.session_state.f_pe == "Sí":
        df_show = df_show[df_show['private_equity_firmas'].apply(has_private_equity)]
    elif st.session_state.f_pe == "No":
        df_show = df_show[~df_show['private_equity_firmas'].apply(has_private_equity)]

    if st.session_state.f_ia == "Sí":
        df_show = df_show[df_show['usa_inteligencia_artificial'].apply(uses_ai)]
    elif st.session_state.f_ia == "No":
        df_show = df_show[~df_show['usa_inteligencia_artificial'].apply(uses_ai)]

    # Filtro Alumni usando el set pre-calculado
    if st.session_state.f_deusto == "Sí":
        df_show = df_show[df_show['Nombre'].isin(empresas_alumni_set)]
    elif st.session_state.f_deusto == "No":
        df_show = df_show[~df_show['Nombre'].isin(empresas_alumni_set)]

    # --- PAGINACIÓN ---
    total_items = len(df_show)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    
    # Control de límites de página
    if st.session_state.current_page >= total_pages: 
        st.session_state.current_page = 0
    if st.session_state.current_page < 0: 
        st.session_state.current_page = 0
        
    start_idx = st.session_state.current_page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    df_page = df_show.iloc[start_idx:end_idx]

    # Barra de resultados
    st.markdown(f"""<div class="results-bar"><div>🎯 <b>{total_items}</b> empresas encontradas</div><div style="font-size: 0.9rem;">Página {st.session_state.current_page + 1} de {max(1, total_pages)}</div></div>""", unsafe_allow_html=True)
    
    # --- RENDERIZADO DE TARJETAS ---
    if not df_page.empty:
        for index, row in df_page.iterrows():
            nombre = row['Nombre']
            provincia = capitalize_first_letter(safe_get_val(row, 'provincia'))
            
            # Contar contactos (lógica inline simplificada para la vista)
            num_contactos = 0
            if not df_alumni.empty:
                # Buscamos coincidencia exacta o parcial
                match = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.strip() == str(nombre).strip()]
                if match.empty:
                    match = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.contains(re.escape(str(nombre).strip()), case=False, na=False)]
                num_contactos = len(match)
            
            with st.expander(f"🏢 **{nombre}** ({provincia})"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Empleados", safe_get_val(row, 'numero_empleados'))
                c2.metric("Ventas Est.", clean_number_format(safe_get_val(row, 'ventas_estimado')))
                pat = str(row.get('patentes', 0))
                c3.metric("Patentes", pat, delta="Innovador" if int(pat) > 0 else None, delta_color="off")
                c4.metric("Contactos", num_contactos, delta="Alumni" if num_contactos > 0 else None, delta_color="off")
                
                st.write("")
                if st.button("➕ Más detalles", key=f"btn_{index}", use_container_width=True):
                    st.session_state.selected_empresa = row['Nombre']
                    st.session_state.page = 'detail'
                    st.session_state.scroll_needed = True
                    st.rerun()
        
        # --- BOTONES DE PAGINACIÓN ---
        st.write("")
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.session_state.current_page > 0:
                if st.button("⬅️ Anterior", use_container_width=True):
                    st.session_state.current_page -= 1
                    st.session_state.scroll_needed = True
                    st.rerun()
        with col_next:
            if st.session_state.current_page < total_pages - 1:
                if st.button("Siguiente ➡️", use_container_width=True):
                    st.session_state.current_page += 1
                    st.session_state.scroll_needed = True
                    st.rerun()
    else: 
        st.warning("No hay empresas que coincidan con estos filtros.")