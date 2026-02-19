import streamlit as st
import pandas as pd
import re
from utils.helpers import (
    clean_number_format, safe_get_val, capitalize_first_letter, 
    render_table, get_hierarchy_order
)

def show_detail(nombre_empresa, df_main, df_alumni):
    # Buscar datos de la empresa
    row_data = df_main[df_main['Nombre'] == nombre_empresa]
    
    if row_data.empty:
        st.error("Error: No se encontraron datos de la empresa.")
        if st.button("Volver"):
            st.session_state.page = 'explorer'
            st.rerun()
        return

    r = row_data.iloc[0]
    
    # --- BOTONES DE NAVEGACIÓN (ARRIBA) ---
    col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
    with col_nav1:
        if st.button("⬅️ Explorador", use_container_width=True):
            st.session_state.page = 'explorer'
            st.rerun()
    with col_nav3:
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    st.divider()
    
    # --- TÍTULO ---
    st.title(f"🏢 {safe_get_val(r, 'Nombre')}")
    
    # 1. RESUMEN
    st.markdown('<div class="section-title">Resumen</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="kpi-card"><div class="kpi-value">{capitalize_first_letter(safe_get_val(r, "provincia"))}</div><div class="kpi-label">UBICACIÓN</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-card"><div class="kpi-value">{safe_get_val(r, "veredicto_final")}</div><div class="kpi-label">CLASIFICACIÓN BINGO</div></div>', unsafe_allow_html=True)
    
    v_raw = safe_get_val(r, "conclusion_sueldo_80k")
    v_color = "#2E7D32" if "VIABLE" in v_raw.upper() else "#C62828" if "DIFICIL" in v_raw.upper() else "#1F4E79"
    v_text = "VIABLE" if "VIABLE" in v_raw.upper() else "DIFÍCIL" if "DIFICIL" in v_raw.upper() else "NEUTRO"
    c3.markdown(f'<div class="kpi-card"><div class="kpi-value" style="color:{v_color}">{v_text}</div><div class="kpi-label">VIABILIDAD SALARIAL</div></div>', unsafe_allow_html=True)
    
    render_table(pd.DataFrame({
        "Ventas Est.": [clean_number_format(safe_get_val(r, 'ventas_estimado'))],
        "Empleados": [clean_number_format(safe_get_val(r, 'numero_empleados'))],
        "Patentes": [str(r.get('patentes', 0))],
        "Año Const.": [safe_get_val(r, 'ano_constitucion')],
        "Web": [safe_get_val(r, 'web_oficial')]
    }))

    # 2. SECTOR Y ACTIVIDAD
    st.markdown('<div class="section-title">Sector y Actividad</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="responsive-grid">
        <div class="content-box">
            <span class="box-header">Sector</span>
            {safe_get_val(r, 'SECTOR_NOMBRE')}
        </div>
        <div class="content-box">
            <span class="box-header">Actividad Principal</span>
            {safe_get_val(r, 'actividad_resumen')}
        </div>
    </div>""", unsafe_allow_html=True)

    # 3. PROPIEDAD Y SOLVENCIA
    st.markdown('<div class="section-title">Propiedad y Solvencia</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="responsive-grid">
        <div class="content-box">
            <span class="box-header">Estructura de la Propiedad</span>
            <b>Accionistas:</b> {safe_get_val(r, 'propiedad_accionistas')}<br><br>
            <b>Private Equity:</b> {safe_get_val(r, 'private_equity_firmas')}
        </div>
        <div class="content-box">
            <span class="box-header">Finanzas y Solvencia</span>
            <b>Financiación Pública:</b> {safe_get_val(r, 'financiacion_publica_detalle')}<br><br>
            <b>Solvencia:</b> {safe_get_val(r, 'solvencia_txt')}
        </div>
    </div>""", unsafe_allow_html=True)

    # 4. MADUREZ TECNOLÓGICA
    st.markdown('<div class="section-title">Madurez Tecnológica</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="grid-2">
        <div class="tech-hero"><div class="tech-hero-label">CTO / Responsable</div><div class="tech-hero-val">{safe_get_val(r, 'cto_actual')}</div></div>
        <div class="tech-hero"><div class="tech-hero-label">Equipo Ingeniería</div><div class="tech-hero-val">{safe_get_val(r, 'tamano_ing')}</div></div>
    </div>
    <div class="grid-3">
        <div class="tech-card"><span class="tech-icon">🧠</span><div class="tech-title">IA & Automatización</div><div class="tech-text">{safe_get_val(r, 'usa_inteligencia_artificial')}</div></div>
        <div class="tech-card"><span class="tech-icon">☁️</span><div class="tech-title">Infraestructura</div><div class="tech-text">{safe_get_val(r, 'plataforma_cloud')}</div></div>
        <div class="tech-card"><span class="tech-icon">💻</span><div class="tech-title">Stack Técnico</div><div class="tech-text">{safe_get_val(r, 'perfil_txt')}</div></div>
    </div>""", unsafe_allow_html=True)
    
    # 5. NETWORKING (ALUMNI)
    st.markdown('<div class="section-title">Networking (Alumni)</div>', unsafe_allow_html=True)
    
    match = pd.DataFrame()
    if not df_alumni.empty:
        match = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.strip() == str(nombre_empresa).strip()]
        if match.empty:
            match = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.contains(re.escape(str(nombre_empresa).strip()), case=False, na=False)]

    if not match.empty:
        st.success(f"✅ Se han encontrado {len(match)} contactos en esta empresa.")
        
        if 'jerarquía' in match.columns:
            match['sort_order'] = match['jerarquía'].apply(get_hierarchy_order)
            df_sorted = match.sort_values(by=['sort_order', 'Nombre']).drop('sort_order', axis=1)
        else:
            df_sorted = match.copy()
        
        t1, t2 = st.tabs(["📊 Resumen", "📋 Lista Detallada"])
        
        with t1:
            if 'jerarquía' in df_sorted.columns:
                summary_data = []
                for hierarchy in ['top management', 'middle management', 'entry level/others']:
                    count = len(df_sorted[df_sorted['jerarquía'].astype(str).str.lower().str.strip() == hierarchy])
                    if count > 0:
                        display_name = hierarchy.title() if hierarchy != 'entry level/others' else 'Entry Level/Others'
                        summary_data.append({'Nivel': display_name, 'Total': count, 'key': hierarchy})
                
                if summary_data:
                    df_summary = pd.DataFrame(summary_data)
                    html_sum = '<table class="custom-table" style="width:100%"><thead><tr><th>Nivel Jerárquico</th><th>Cantidad</th></tr></thead><tbody>'
                    for _, row_c in df_summary.iterrows():
                        key = row_c['key']
                        badge = "badge-top" if "top" in key else "badge-mid" if "middle" in key else "badge-entry"
                        html_sum += f'<tr><td><span class="{badge}">{row_c["Nivel"]}</span></td><td style="text-align: center;"><b>{row_c["Total"]}</b></td></tr>'
                    html_sum += '</tbody></table>'
                    st.markdown(html_sum, unsafe_allow_html=True)
                else:
                    st.info("No hay datos de jerarquía disponibles")
            else:
                st.info("Datos de jerarquía no disponibles.")
        
        with t2:
            cols_view = ['Nombre', 'Cargo', 'jerarquía', 'función', 'url_linkedin']
            cols_exist = [c for c in cols_view if c in df_sorted.columns]
            df_display = df_sorted[cols_exist].copy()
            
            if 'Nombre' in df_display.columns:
                df_display['Nombre'] = df_display['Nombre'].apply(lambda x: capitalize_first_letter(x))
            
            if 'jerarquía' in df_display.columns:
                def get_badge(hierarchy):
                    if pd.isna(hierarchy): return '-'
                    h = str(hierarchy).strip().lower()
                    if "top" in h: return f'<span class="badge-top">{h.title()}</span>'
                    elif "middle" in h: return f'<span class="badge-mid">{h.title()}</span>'
                    else: return f'<span class="badge-entry">{h.upper()}</span>'
                df_display['jerarquía'] = df_display['jerarquía'].apply(get_badge)
            
            render_table(df_display)
    else:
        st.info("ℹ️ No hay contactos alumni registrados actualmente en esta empresa.")
    
    st.write("")
    if st.button("⬅️ Volver al Explorador", key="btn_back_bottom", use_container_width=True):
        st.session_state.page = 'explorer'
        st.rerun()