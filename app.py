import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

# Función callback cuando se publica un mensaje
def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

# Función callback cuando se recibe un mensaje
def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write("Mensaje recibido:", message_received)

# Configurar broker MQTT
broker = "broker.hivemq.com"
port = 1883
client1 = paho.Client("APP_yyyyy")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

# Cargar modelo de gestos
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# INTERFAZ STREAMLIT
st.title("🔒 Cerradura Inteligente")

# --- Herramienta 1: Entrada por cámara (reconocimiento de gestos)
st.subheader("🔍 Reconocimiento por Gesto (foto)")
img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    if prediction[0][0] > 0.3:
        st.success('🔓 Abriendo (por gesto)')
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif prediction[0][1] > 0.3:
        st.warning('🔒 Cerrando (por gesto)')
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)

# --- Herramienta 2: Entrada por texto
st.subheader("⌨️ Control por Texto")
user_command = st.text_input("Escribe 'abrir' o 'cerrar'").strip().lower()

if st.button("Enviar comando"):
    if user_command == "abrir":
        st.success("🔓 Abriendo (por texto)")
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif user_command == "cerrar":
        st.warning("🔒 Cerrando (por texto)")
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)
    else:
        st.error("Comando no válido. Escribe 'abrir' o 'cerrar'.")
