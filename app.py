import streamlit as st
import yt_dlp
import os
import tempfile

# Configuración básica
st.set_page_config(page_title="Música para Mamá", page_icon="🎵", layout="centered")

st.markdown("""
<style>
    .titulo { text-align: center; color: #E83E8C; font-size: 32px; font-weight: bold; }
    .stTextInput input { font-size: 18px; padding: 15px; border-radius: 15px; border: 2px solid #F0B2D4; }
    .stButton > button { width: 100%; border-radius: 20px; height: 60px; background-color: #E83E8C; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo'>Descargador de música 🎵</div>", unsafe_allow_html=True)

url = st.text_input("Enlace", placeholder="Pega aquí el enlace de YouTube...", label_visibility="collapsed")

if st.button("¡Descargar!"):
    if url:
        if "YOUTUBE_COOKIES" not in st.secrets:
            st.error("Configuración faltante: Por favor añade el secreto 'YOUTUBE_COOKIES' en Streamlit.")
            st.stop()

        with st.spinner("Descargando... un momento ⏳"):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    cookie_path = os.path.join(temp_dir, "cookies.txt")
                    with open(cookie_path, "w", encoding="utf-8") as f:
                        f.write(st.secrets["YOUTUBE_COOKIES"])

                    # Configuración robusta sin depender de ffmpeg
                    ydl_opts = {
                        'format': 'bestaudio/best', 
                        'outtmpl': os.path.join(temp_dir, 'cancion.%(ext)s'),
                        'cookiefile': cookie_path,
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'ignoreerrors': True,
                        'geo_bypass': True,
                        'geo_bypass_country': 'ES',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        titulo = info.get('title', 'cancion')
                    
                    # Buscar el archivo descargado (yt-dlp decide la extensión, ej: .m4a o .webm)
                    archivos = [f for f in os.listdir(temp_dir) if f.startswith('cancion.')]
                    
                    if archivos:
                        archivo_final = os.path.join(temp_dir, archivos[0])
                        with open(archivo_final, "rb") as f:
                            data = f.read()
                        
                        st.success("¡Listo!")
                        st.download_button(
                            label="Descargar archivo",
                            data=data,
                            file_name=f"{titulo}.m4a",
                            mime="audio/mp4"
                        )
                    else:
                        st.error("No se pudo obtener el archivo. Prueba con otro enlace.")
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Pega un enlace primero.")
