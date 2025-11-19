import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import paho.mqtt.client as paho
import json
# Las librerías gTTS y googletrans no son estrictamente necesarias para el control MQTT
# por lo que se omiten para simplificar, pero puedes reintroducirlas si las necesitas.

# --- CONFIGURACIÓN Y OPTIMIZACIÓN MQTT ---
broker = "broker.mqttdashboard.com"
port = 1883
topic_publish = "voice_ctrl_jsq"
client_id = "GIT-HUB-jsq_Voz"

# Funciones de Callback (Se mantienen para completar el código, aunque no se usen activamente)
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    message_received = str(message.payload.decode("utf-8"))
    print(f"Mensaje recibido: {message_received}")
    pass

# Inicialización y Conexión del Cliente Único
@st.cache_resource
def get_mqtt_client_voice():
    client = paho.Client(client_id)
    client.on_publish = on_publish
    client.on_message = on_message
    try:
        client.connect(broker, port)
        client.loop_start() 
        print(f"Cliente MQTT '{client_id}' conectado.")
    except Exception as e:
        st.error(f"Error al conectar el cliente MQTT: {e}")
    return client

mqtt_client_voice = get_mqtt_client_voice()

# --- INTERFAZ DE USUARIO (STREAMLIT) ---

st.title("INTERFACES MULTIMODALES")
st.subheader("CONTROL POR VOZ")

# Intenta cargar la imagen si existe, si no, usa un marcador de posición.
try:
    image = Image.open('voice_ctrl.jpg')
    st.image(image, width=200)
except FileNotFoundError:
    st.info("[Imagen 'voice_ctrl.jpg' no encontrada. Usando marcador de posición.]")


st.write("Toca el Botón y habla ")

# Configuración del botón STT (Speech-to-Text) de Bokeh
stt_button = Button(label=" Inicio ", width=200)

# Código JavaScript para la API de reconocimiento de voz
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false; // Cambiado a false para una sola frase
    recognition.interimResults = false; // Cambiado a false para solo resultados finales
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            // Envía la transcripción como un evento a Streamlit
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

# Muestra el botón y espera el resultado
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

# Procesamiento del Resultado de Voz
if result:
    if "GET_TEXT" in result:
        transcribed_text = result.get("GET_TEXT").strip().lower() # Normalizamos a minúsculas
        st.write(f"Voz detectada: **{transcribed_text}**")
        
        # 1. Publicar el comando MQTT
        try:
            # El comando de voz completo se envía bajo la clave "Act1"
            message = json.dumps({"Act1": transcribed_text})
            ret = mqtt_client_voice.publish(topic_publish, message)
            
            if ret.rc == paho.MQTT_ERR_SUCCESS:
                st.success(f"Comando de voz enviado: {transcribed_text}")
            else:
                st.warning(f"Error al enviar comando MQTT: {ret.rc}")

        except Exception as e:
            st.error(f"Error al procesar el comando MQTT: {e}")

        # La lógica de os.mkdir("temp") es para TTS/Traducción y no afecta a MQTT.
