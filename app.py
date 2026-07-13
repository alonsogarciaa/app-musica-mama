import streamlit as st
import yt_dlp
import os
import tempfile

# 1. Configuración de la página (Debe ser la primera instrucción)
st.set_page_config(page_title="Música para Mamá", page_icon="🎵", layout="centered")

# 2. Inyección de CSS para diseño móvil, limpio y amigable
st.markdown("""
<style>
    /* Ocultar el menú superior y el pie de página por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Título principal */
    .titulo-mama {
        text-align: center;
        color: #E83E8C; /* Rosa suave/fuerte */
        font-family: 'Arial', sans-serif;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* Hacer el input de texto más grande */
    .stTextInput input {
        font-size: 18px !important;
        padding: 15px !important;
        border-radius: 15px !important;
        border: 2px solid #F0B2D4 !important;
    }
    
    /* Estilizar TODOS los botones para que sean gigantes y fáciles de pulsar */
    .stButton > button, div[data-testid="stDownloadButton"] > button {
        width: 100%;
        border-radius: 20px;
        height: 70px;
        font-size: 20px !important;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Botón de buscar (Rosa) */
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

# Campo de texto sin etiqueta visible para mantenerlo limpio
url = st.text_input("", placeholder="Pega aquí el enlace de tu canción...")

st.write("") # Espacio en blanco

# 4. Lógica de descarga
if st.button("¡Descargar Música!"):
    if url:
        with st.spinner("Buscando tu canción... un momento, por favor ⏳"):
            try:
                # Usamos un directorio temporal para no saturar el servidor
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Forzamos que el archivo de salida se llame siempre "cancion" para evitar 
                    # problemas de caracteres raros en el sistema operativo.
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(temp_dir, 'cancion.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                        'no_warnings': True
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Extraer info para obtener el título real de la canción
                        info_dict = ydl.extract_info(url, download=True)
                        titulo_real = info_dict.get('title', 'Cancion_Descargada')
                        
                        # Limpiar el título de caracteres problemáticos para el nombre del archivo
                        titulo_limpio = "".join(x for x in titulo_real if x.isalnum() or x in " -_")
                        
                        archivo_mp3 = os.path.join(temp_dir, "cancion.mp3")

                        if os.path.exists(archivo_mp3):
                            with open(archivo_mp3, "rb") as file:
                                audio_bytes = file.read()

                            st.success("¡Canción encontrada y lista! 🎉")
                            
                            # Botón de descarga final (Streamlit lo coloreará por defecto o aplicará nuestro CSS)
                            st.download_button(
                                label="Guardar canción en mi móvil 📥",
                                data=audio_bytes,
                                file_name=f"{titulo_limpio}.mp3",
                                mime="audio/mpeg",
                                type="primary" # Lo hace destacar más
                            )
                        else:
                            st.error("¡Ups! Parece que el enlace no es correcto. Inténtalo de nuevo, por favor ❤️")
            except Exception as e:
                # Mensaje genérico de error para no confundirla con códigos
                st.error("¡Ups! Parece que el enlace no es correcto o es privado. Inténtalo de nuevo, por favor ❤️")
    else:
        st.warning("Por favor, pega un enlace primero para poder buscarla. 😊")
