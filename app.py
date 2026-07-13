import streamlit as st
import yt_dlp
import os
import tempfile

# 1. Configuración de la página
st.set_page_config(page_title="Música para Mamá", page_icon="🎵", layout="centered")

# 2. Inyección de CSS
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

# 3. Interfaz de Usuario
st.markdown("<div class='titulo-mama'>El descargador de música de Mamá 🎵</div>", unsafe_allow_html=True)

# SOLUCIÓN 1: Le damos un nombre pero usamos label_visibility="collapsed" para ocultarlo
url = st.text_input(
    "Enlace de YouTube", 
    placeholder="Pega aquí el enlace de tu canción...", 
    label_visibility="collapsed"
)

st.write("") 

# 4. Lógica de descarga
if st.button("¡Descargar Música!"):
    if url:
        with st.spinner("Buscando tu canción... un momento, por favor ⏳"):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    
                    # SOLUCIÓN 2: Añadimos trucos antibloqueo a yt-dlp
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(temp_dir, 'cancion.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                        'no_warnings': True,
                        # Engañamos a YouTube haciéndonos pasar por un móvil Android
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android', 'web']
                            }
                        },
                        'nocheckcertificate': True # Evita problemas de seguridad en el servidor
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
                            st.error("¡Ups! Parece que el enlace no es correcto. Inténtalo de nuevo, por favor ❤️")
            except Exception as e:
                st.error("¡Ups! YouTube nos ha bloqueado temporalmente o el enlace es privado. Inténtalo con otra canción ❤️")
                # Imprimimos el error real en la consola de Streamlit para que tú lo veas, 
                # pero tu madre solo verá el mensaje rojo de arriba.
                print(f"Error técnico: {e}")
    else:
        st.warning("Por favor, pega un enlace primero para poder buscarla. 😊")
