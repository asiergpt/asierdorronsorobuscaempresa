import streamlit as st
import pandas as pd

def show_entidades(df_entidades):
    st.title("🏛️ Ecosistema Vasco")
    st.markdown("Navega por las distintas categorías para conocer a los "
                "jugadores clave que impulsan la industria y tecnología local.")
    
    # Navegación superior
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("⬅️ Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    st.divider()

    if df_entidades.empty:
        st.warning("⚠️ No se ha encontrado el archivo 'ecosistema_vasco.csv' o está vacío.")
        return

    # Extraer categorías únicas para hacer pestañas (Tabs)
    categorias = sorted(df_entidades['CATEGORÍA'].dropna().unique())
    
    if categorias:
        # Crea pestañas dinámicamente según las categorías del CSV
        tabs = st.tabs([cat.title() for cat in categorias])
        
        for i, cat in enumerate(categorias):
            with tabs[i]:
                # Filtrar entidades de esta categoría
                df_cat = df_entidades[df_entidades['CATEGORÍA'] == cat]
                
                # Mostrar cada entidad como una "tarjeta" desplegable
                for _, row in df_cat.iterrows():
                    nombre = row.get('NOMBRE', 'Sin nombre')
                    ciudad = row.get('Ciudad', '-')
                    definicion = row.get('DEFINICION', 'Sin descripción')
                    web = row.get('Web', '#')
                    
                    with st.expander(f"📌 **{nombre}** — 📍 {ciudad}"):
                        st.markdown(f"**¿Qué hacen?**<br> {definicion}", unsafe_allow_html=True)
                        st.write("")
                        if web and web != '#':
                            st.markdown(f"🌐 [Visitar Web Oficial]({web})")
    else:
        st.info("No hay categorías definidas en los datos.")