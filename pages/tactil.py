import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("GIT-HUB-jsq")
client1.on_message = on_message



st.title("🏡 Control Remoto Inteligente (MQTT)")

st.header("💡 Control de Iluminación")

# Creación de tres columnas para los botones de las luces
col1, col2, col3 = st.columns(3)

# Columna 1: Luces Sala (L)
with col1:
    st.subheader("Hall (H)")
    if st.button('H ON'):
        act1="lights on"
        client1= paho.Client("GIT-HUB-jsq")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message =json.dumps({"Act1":act1})
        ret= client1.publish("voice_ctrl_jsq", message)
     
        #client1.subscribe("Sensores")
        
    else:
        st.write('')
    
    if st.button('H OFF'):
        act1="lights off"
        client1= paho.Client("GIT-HUB-jsq")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message =json.dumps({"Act1":act1})
        ret= client1.publish("voice_ctrl_jsq", message)
        
    else:
        st.write('')


# Columna 2: Habitación (R)
with col2:
    st.subheader("Baño (B)")
    if st.button('B ON'):
        act1="room on"
        client1= paho.Client("GIT-HUB-jsq")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message =json.dumps({"Act1":act1})
        ret= client1.publish("voice_ctrl_jsq", message)
    
    if st.button('B OFF'):
        act1="room off"
        client1= paho.Client("GIT-HUB-jsq")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message =json.dumps({"Act1":act1})
        ret= client1.publish("voice_ctrl_jsq", message)

# Columna 3: Mi Habitación (MR)
with col3:
    st.subheader("Mi Habitación (MR)")
    if st.button('MR ON'):
        act1="my room on"
        client1= paho.Client("GIT-HUB-jsq")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message =json.dumps({"Act1":act1})
        ret= client1.publish("voice_ctrl_jsq", message)
    
    if st.button('MR OFF'):
        act1="my room off"
        client1= paho.Client("GIT-HUB-jsq")                           
        client1.on_publish = on_publish                          
        client1.connect(broker,port)  
        message =json.dumps({"Act1":act1})
        ret= client1.publish("voice_ctrl_jsq", message)


st.header("⚙️ Control Analógico y Otros")

values = st.slider('Selecciona el rango de valores',0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("voice_ctrl_jsq", message)
    
 
else:
    st.write('')
