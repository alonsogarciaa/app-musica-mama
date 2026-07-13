import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Música para Mamá", page_icon="🎵", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .titulo-mama {
        text-align: center;
        color: #E83E8C;
        font-family: 'Arial', sans-serif;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .stTextInput input {
        font-size: 18px !important;
        padding: 15px !important;
        border-radius: 15px !important;
        border: 2px solid #F0B2D4 !important;
    }
    
    .stButton > button, div[data-testid="stDownloadButton"] > button {
        width: 100%;
        border-radius: 20px;
        height: 70px;
        font-size: 20px !important;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton > button {
        background-color: #E83E8C;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #D63384;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-mama'>El descargador de música de Mamá 🎵</div>", unsafe_allow_html=True)

url = st.text_input(
    "Enlace de YouTube", 
    placeholder="Pega aquí el enlace de tu canción...", 
    label_visibility="collapsed"
)

st.write("") 

if st.button("¡Descargar Música!"):
    if url:
        # 1. Comprobación de seguridad: ¿Existen las cookies en los secretos?
        if "YOUTUBE_COOKIES" not in st.secrets:
            st.error("🔧 ¡Aviso para el desarrollador! Faltan las cookies en los Secrets de Streamlit.")
            st.stop()

        with st.spinner("Buscando tu canción... un momento, por favor ⏳"):
            try:
                # 2. Carpeta temporal para guardar las cookies y el MP3
                with tempfile.TemporaryDirectory() as temp_dir:
                    
                    # 3. Fabricamos el archivo de cookies sobre la marcha
                    cookie_path = os.path.join(temp_dir, "cookies.txt")
                    with open(cookie_path, "w", encoding="utf-8") as f:
                        f.write(st.secrets["YOUTUBE_COOKIES"])
                    # 4. Le pasamos el archivo a yt-dlp
                   ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(temp_dir, 'cancion.%(ext)s'),
                        'cookiefile': cookie_path,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'ignoreerrors': True,
                        # Nueva configuración para evitar restricciones geográficas
                        'geo_bypass': True,
                        'geo_bypass_country': 'ES',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(url, download=True)
                        titulo_real = info_dict.get('title', 'Cancion_Descargada')
                        
                        titulo_limpio = "".join(x for x in titulo_real if x.isalnum() or x in " -_")
                        archivo_mp3 = os.path.join(temp_dir, "cancion.mp3")

                        if os.path.exists(archivo_mp3):
                            with open(archivo_mp3, "rb") as file:
                                audio_bytes = file.read()

                            st.success("¡Canción encontrada y lista! 🎉")
                            
                            st.download_button(
                                label="Guardar canción en mi móvil 📥",
                                data=audio_bytes,
                                file_name=f"{titulo_limpio}.mp3",
                                mime="audio/mpeg",
                                type="primary" 
                            )
                        else:
                            st.error("¡Ups! Parece que el enlace no es correcto. Inténtalo de nuevo ❤️")
            except Exception as e:
                # Si falla, te imprimimos a ti el error técnico por consola, y a tu madre un texto amable
                print(f"Detalle del error: {e}")
                st.error("¡Ups! No hemos podido descargar esta canción. Comprueba el enlace o prueba con otra ❤️")
    else:
        st.warning("Por favor, pega un enlace primero para poder buscarla. 😊")
