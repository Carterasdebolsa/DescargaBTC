import streamlit as st
import pandas as pd
import numpy as np
import pytz
import plotly.express as px

# Configurar el diseño
st.set_page_config(layout="wide") 
@st.cache_data(ttl=60)  # Opcionalmente puedes caché el CSV durante 1 minuto
def load_data():
    # URL directa al archivo CSV en tu repositorio de GitHub
    url = 'https://raw.githubusercontent.com/Carterasdebolsa/DescargaBTC/main/btc_data.csv'
    data = pd.read_csv(url)
    data = pd.DataFrame(data)

    # Asegurarse de que la columna de fecha sea del tipo datetime
    data['Date'] = pd.to_datetime(data['Date'])  # Cambia 'fecha' por el nombre real de la columna de fecha si es diferente
    
    data.set_index('Date', inplace=True)  # Establecer la columna de fecha como índice

    return data

# Cargar y mostrar los datos
BTC = load_data()

# Asegúrate de que el índice es un DatetimeIndex
if BTC.index.tz is None:
    BTC.index = BTC.index.tz_localize('UTC').tz_convert('Europe/Madrid')
else:
    BTC.index = BTC.index.tz_convert('Europe/Madrid')  # Solo convertir si ya tiene zona horaria

# Eliminar la hora del índice, manteniendo solo la fecha
BTC.index = BTC.index.date # Opción para mantener formato datetime64 con horas en 00:00:00



# Mostrar los datos en el dashboard
st.dataframe(BTC.iloc[::-1].round(2), use_container_width=True)



# Crear el gráfico de línea con escala logarítmica
fig = px.line(
    BTC, 
    x=BTC.index, 
    y="Close", 
    title="Bitcoin escala logarítmica", 
    log_y=True, 
    labels={"Close": "Precio", "index": "Fecha"}
)

# Formato para mostrar día, mes y año en el tooltip
fig.update_traces(hovertemplate='%{x|%d-%m-%Y}<br>Precio: %{y:.2f}')


# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

st.sidebar.header("Opciones")
st.sidebar.write("Aquí puedes agregar opciones de usuario.")  
