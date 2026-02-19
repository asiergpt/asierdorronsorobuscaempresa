import streamlit as st
import base64
import os

# --- FUNCIÓN AUXILIAR PARA IMÁGENES ---
def get_image_base64(path):
    """Convierte una imagen local en una cadena base64 para incrustar en HTML"""
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 12a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm9 11a1 1 0 0 1-2 0v-2a3 3 0 0 0-3-3H8a3 3 0 0 0-3 3v2a1 1 0 0 1-2 0v-2a5 5 0 0 1 5-5h8a5 5 0 0 1 5 5v2z' fill='rgba(255,255,255,0.2)'/%3E%3C/svg%3E"

def show_home():
    # --- PREPARAR IMAGEN ---
    img_path = os.path.join("assets", "foto_perfil.png")
    img_base64 = get_image_base64(img_path)
    
# --- HERO SECTION CON FOTO ---
# --- HERO SECTION CON FOTO ---
    st.markdown(f"""
    <style>
        .hero-container {{ display: flex; align-items: center; justify-content: center; gap: 40px; flex-wrap: wrap; text-align: left; }}
        .profile-avatar {{ width: 180px; height: 180px; border-radius: 50%; border: 5px solid rgba(255,255,255,0.2); object-fit: cover; box-shadow: 0 10px 25px rgba(0,0,0,0.25); }}
        .hero-text {{ max-width: 600px; }}
        @media (max-width: 768px) {{ .hero-container {{ text-align: center; flex-direction: column; gap: 20px; }} .hero-text {{ margin-bottom: 20px; }} }}
    </style>
    <div style="background: linear-gradient(135deg, #1F4E79 0%, #0D253F 100%); padding: 50px 30px; border-radius: 20px; color: white; box-shadow: 0 10px 40px rgba(31, 78, 121, 0.3); margin-bottom: 30px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -60px; right: -60px; width: 250px; height: 250px; background: rgba(255,255,255,0.04); border-radius: 50%; z-index: 0;"></div>
        <div class="hero-container" style="position: relative; z-index: 1;">
            <img src="{img_base64}" alt="Asier Dorronsoro" class="profile-avatar">
            <div class="hero-text">
                <div style="margin-bottom: 15px;"></div>
                <h1 style="font-size: 3.2em; font-weight: 800; margin: 0 0 15px 0; letter-spacing: -1px; line-height: 1.1; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                    Asier Dorronsoro
                </h1>
                <p style="font-size: 1.25em; margin: 0 0 25px 0; opacity: 0.95; font-weight: 300; line-height: 1.5;">
                    <strong>Objetivo: </strong>Buscar mi siguiente reto profesional. <span style="white-space: nowrap;">Viviendo en San Sebastián.</span>
                </p>
                <a href="https://www.linkedin.com/in/asierdorronsoro/" target="_blank" style="text-decoration: none; background: white; color: #1F4E79; padding: 12px 28px; border-radius: 30px; font-weight: 700; font-size: 1em; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.15); display: inline-block; border: 2px solid white;">
                    🚀 Conectar en LinkedIn
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- CARDS SECTION (3 COLUMNAS) ---
    st.markdown("<style>.card-ecosistema { border-top-color: #2E7D32; }</style>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card card-empresas">
            <div class="card-icon">🏢</div>
            <h3>Empresas</h3>
            <p>Busca y descubre empresas de Gipuzkoa, Bizkaia, Araba y Navarra</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver →", key="btn_home_empresas", use_container_width=True):
            st.session_state.page = 'explorer'
            st.session_state.scroll_needed = True
            st.session_state.selected_empresa = None
            st.session_state.current_page = 0
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class="card card-profesionales">
            <div class="card-icon">👥</div>
            <h3>Profesionales</h3>
            <p>Busca y conecta con profesionales.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver →", key="btn_home_personas", use_container_width=True):
            st.session_state.page = 'personas'
            st.session_state.scroll_needed = True
            st.rerun()

    with col3:
        st.markdown("""
        <div class="card card-ecosistema">
            <div class="card-icon">🏛️</div>
            <h3>Ecosistema</h3>
            <p>Descubre centros tecnológicos, clústeres y agencias públicas.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver →", key="btn_home_ecosistema", use_container_width=True):
            st.session_state.page = 'entidades'
            st.session_state.scroll_needed = True
            st.rerun()
    
    st.write("")
    
    # --- NOTA ---
    st.markdown("""
    <div class="note-section">
        <p><strong>📌 Nota:</strong> Los datos provienen de inteligencia artificial e información pública (prensa, rankings, webs corporativas). Aunque procuro precisión, algunos datos pueden ser incompletos o inexactos.</p>
    </div>
    """, unsafe_allow_html=True)