import streamlit as st
import pandas as pd
import pickle
import numpy as np
import joblib
import numpy as np

# Cargar el modelo entrenado
with open('c://users//Sergi//proyectos//proyecto_final//models//Modelo_RF_datos_escalados', 'rb') as f:
    modelo = pickle.load(f)

# Cargar el diccionario de factorización
factorization_dict = pd.read_csv('c://users//Sergi//proyectos//proyecto_final//src//factorization_dict.csv')

# Cargar la información de escalado
with open('C://Users//sergi//Proyectos//Proyecto_Final//src//fit_transform.pkl', 'rb') as f:
    scaler = joblib.load(f)

# Crear un diccionario de mapeo inverso a partir del diccionario de factorización
inverse_factorization_dict = {col: {str(val): key for key, val in factorization_dict[col].items()} for col in factorization_dict.columns}

st.image('c://users//Sergi//proyectos//logo.jpg', width=100) 

# Título de la aplicación con estilo
st.title(":blue[Tasa y vende tu auto en 1 día]")
st.divider()
st.subheader("Olvídate de la burocracia! Cambia o vende en línea y en menos de 24 hrs", divider='blue')

# Convertir las selecciones del usuario de nuevo a las variables originales
def inverse_factorize(column, value):
    return inverse_factorization_dict[column][str(value)]

# Espaciado entre los elementos de entrada y el botón de predicción
st.markdown("---")

# Selección de opciones por parte del usuario
manufacturer = st.selectbox('Fabricante', [''] + list(inverse_factorization_dict['manufacturer'].keys()), key='manufacturer')
model_input = st.selectbox('Modelo', [''] + list(inverse_factorization_dict['model'].keys()), key='model')
year = st.number_input('Año', min_value=1997, max_value=2022, value=2010, key='year')
odometer = st.number_input('Odómetro (millas)', min_value=0, key='odometer')
fuel = st.selectbox('Combustible', [''] + list(inverse_factorization_dict['fuel'].keys()), key='fuel')
transmission = st.selectbox('Transmisión', [''] + list(inverse_factorization_dict['transmission'].keys()), key='transmission')
drive = st.selectbox('Tracción', [''] + list(inverse_factorization_dict['drive'].keys()), key='drive')
size = st.selectbox('Tamaño', [''] + list(inverse_factorization_dict['size'].keys()), key='size')
type_ = st.selectbox('Tipo de Vehículo', [''] + list(inverse_factorization_dict['type'].keys()), key='type')
state = st.selectbox('Estado', [''] + list(inverse_factorization_dict['state'].keys()), key='state')
manufacturer_original = manufacturer
model_original = model_input
# Espaciado entre los elementos de entrada y el botón de predicción
st.markdown("---")

# Botón para predecir el precio con un estilo más llamativo
if st.button('Tasar Auto', key='submit_button'):
    # Convertir las selecciones del usuario de nuevo a las variables originales
    manufacturer = inverse_factorize('manufacturer', manufacturer)
    model_input = inverse_factorize('model', model_input)
    fuel = inverse_factorize('fuel', fuel)
    transmission = inverse_factorize('transmission', transmission)
    drive = inverse_factorize('drive', drive)
    size = inverse_factorize('size', size)
    type_ = inverse_factorize('type', type_)
    state = inverse_factorize('state', state)
    
    # Crear un DataFrame con los datos ingresados
    data = pd.DataFrame({
        'year': [year],
        'manufacturer': [manufacturer],
        'model': [model_input],
        'fuel': [fuel],
        'odometer': [odometer],
        'transmission': [transmission],
        'drive': [drive],
        'size': [size],
        'type': [type_],
        'state': [state]
    })
    
    # Escalar los datos ingresados por el usuario
    data_scaled = scaler.transform(data)
    
    # Realizar la predicción
    prediction = modelo.predict(data_scaled)
    # Se oferta el 75% del valor predico
    oferta = 0.75 * prediction[0]
    st.markdown(
    f"<h2 style='color: #FFFFFF;'>La oferta estimada por tu {manufacturer_original} {model_original} será de: ${oferta:,.2f}</h2>", 
    unsafe_allow_html=True
        )
    
    # Añadir el botón "Agende su visita"
    if st.button('Agende su visita'):
        pass
