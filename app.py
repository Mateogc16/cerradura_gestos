st.title("🛡️ Portal Encantado de la Fortaleza")

st.markdown("### ✨ *Invoca con tu gesto o palabra el poder de abrir o sellar la puerta mágica...*")

# --- Herramienta 1: Entrada por cámara (reconocimiento de gestos)
st.subheader("📜 Magia Visual - Sello por Gesto")
img_file_buffer = st.camera_input("📸 Muestra tu gesto sagrado frente al espejo encantado")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    if prediction[0][0] > 0.3:
        st.success("🔓 ¡La puerta de roble se abre con tu gesto mágico!")
        client1.publish("PIPPO", "{'gesto': 'Abre'}", qos=0, retain=False)
    elif prediction[0][1] > 0.3:
        st.warning("🔒 ¡El portón se cierra con el poder de tu sello ancestral!")
        client1.publish("PIPPO", "{'gesto': 'Cierra'}", qos=0, retain=False)

# --- Herramienta 2: Entrada por texto
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
