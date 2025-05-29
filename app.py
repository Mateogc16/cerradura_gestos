import paho.mqtt.client as paho
import time
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(page_title="🔐 Portal de la Fortaleza", page_icon="🛡️", layout="centered")

# ---- ESTILO VISUAL MEDIEVAL CON IMAGEN DE FONDO DESDE GITHUB ----
st.markdown(f"""
    <style>
    body {{
        background-color: #000000;
        color: #f3e9dc;
    }}
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/Mateogc16/cerradura_gestos/main/dragon.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    h1, h2, h3 {{
        color: #f8e8c1;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000;
    }}
    .stButton>button {{
        background-color: #5e3929 !important;
        color: #f3e9dc !important;
        border-radius: 10px;
        border: 2px solid #e0c097;
        font-weight: bold;
    }}
    .stTextInput>div>div>input {{
        background-color: #fffbe6;
        color: #3e2f1c;
        border: 1px solid #bfa27f;
    }}
    .block-container {{
        padding-top: 2rem;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        padding: 2rem;
    }}
    </style>
""", unsafe_allow_html=True)

# ---- MQTT ----
def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write("📜 Mensaje recibido:", message_received)

broker = "broker.hivemq.com"
port = 1883
client1 = paho.Client("APP_yyyyy")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

# ---- MODELO ----
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
   #To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0]>0.3:
      st.header('Abriendo')
      client1.publish("IMIA","{'gesto': 'Abre'}",qos=0, retain=False)
      time.sleep(0.2)
    if prediction[0][1]>0.3:
      st.header('Cerrando')
      client1.publish("IMIA","{'gesto': 'Cierra'}",qos=0, retain=False)
      time.sleep(0.2)  

# ---- HERRAMIENTA 2: COMANDO ESCRITO ----
st.subheader("📖 Hechizo Escrito - Sello por Palabra")
user_command = st.text_input("✍️ Escribe 'abrir' o 'cerrar' como si fueran conjuros").strip().lower()

if st.button("🔮 Invocar Hechizo"):
    if user_command == "abrir":
        st.success("🔓 ¡Hechizo aceptado! La entrada se abre ante ti.")
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif user_command == "cerrar":
        st.warning("🔒 ¡Puerta cerrada! El conjuro ha sido sellado.")
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)
    else:
        st.error("🚫 Palabra no reconocida por los grimorios. Usa 'abrir' o 'cerrar'.")
