import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- CONFIGURACIÓN Y OPTIMIZACIÓN MQTT ---
broker = "broker.mqttdashboard.com"
port = 1883
topic_publish = "voice_ctrl_jsq"
# El ID debe ser único para cada cliente.
client_id = "GIT-HUB-jsq_Botones" 

# Funciones de Callback
def on_publish(client, userdata, result):
    print("El dato ha sido publicado")
    pass

def on_message(client, userdata, message):
    message_received = str(message.payload.decode("utf-8"))
    print(f"Mensaje recibido: {message_received}")
    # Nota: Mostrar en la UI fuera del hilo principal de Streamlit requiere st.session_state o threads.
    pass

# Inicialización y Conexión del Cliente Único
@st.cache_resource
def get_mqtt_client():
    client = paho.Client(client_id)
    client.on_publish = on_publish
    client.on_message = on_message
    try:
        client.connect(broker, port)
        client.loop_start()  # Iniciar el hilo de loop para manejar la comunicación en segundo plano
        print(f"Cliente MQTT '{client_id}' conectado.")
    except Exception as e:
        st.error(f"Error al conectar el cliente MQTT: {e}")
    return client

mqtt_client = get_mqtt_client()

# Función centralizada para publicar
def publish_command(action_message, key_name="Act1"):
    message = json.dumps({key_name: action_message})
    ret = mqtt_client.publish(topic_publish, message)
    if ret.rc == paho.MQTT_ERR_SUCCESS:
        st.toast(f"Comando '{action_message}' enviado correctamente.")
    else:
        st.warning(f"Error al enviar comando: {ret.rc}")


# --- INTERFAZ DE USUARIO (STREAMLIT) ---

st.title("🏡 Control Remoto Inteligente (MQTT)")
st.caption(f"Cliente: {client_id} | Python: {platform.python_version()}")

st.header("💡 Control de Iluminación")

# Creación de tres columnas
col1, col2, col3 = st.columns(3)

# Columna 1: Hall (H) - Comandos: "lights on", "lights off"
with col1:
    st.subheader("Hall (H)")
    if st.button('H ON', key='H_ON', use_container_width=True):
        publish_command("lights on")
    if st.button('H OFF', key='H_OFF', use_container_width=True):
        publish_command("lights off")

# Columna 2: Baño (B) - Comandos: "room on", "room off"
with col2:
    st.subheader("Baño (B)")
    if st.button('B ON', key='B_ON', use_container_width=True):
        publish_command("room on")
    if st.button('B OFF', key='B_OFF', use_container_width=True):
        publish_command("room off")

# Columna 3: Mi Habitación (MR) - Comandos: "my room on", "my room off"
with col3:
    st.subheader("Mi Habitación (MR)")
    if st.button('MR ON', key='MR_ON', use_container_width=True):
        publish_command("my room on")
    if st.button('MR OFF', key='MR_OFF', use_container_width=True):
        publish_command("my room off")


st.header("⚙️ Control Analógico y Servomotor")

# Slider para el valor analógico
values = st.slider('Selecciona el valor analógico (0.0 a 100.0)', 0.0, 100.0, key='analog_slider')
st.caption(f'Valor actual del Slider: **{values:.2f}**')

col_analog, col_door = st.columns(2)

with col_analog:
    if st.button('Enviar Valor Analógico', key='send_analog', use_container_width=True):
        # Envía el valor del slider bajo la clave "Analog"
        publish_command(float(values), key_name="Analog")

with col_door:
    st.subheader("Control de Puerta")
    # Nota: Se usan comandos compatibles con la lógica de voz/servomotor del ESP32
    if st.button('Abrir Puerta', key='DOOR_OPEN', use_container_width=True):
        publish_command("open the door", key_name="Act1") # Comando para el servomotor
    if st.button('Cerrar Puerta', key='DOOR_CLOSE', use_container_width=True):
        publish_command("close the door", key_name="Act1") # Comando para el servomotor
