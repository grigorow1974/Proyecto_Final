import streamlit as st
import pandas as pd
import pickle

# Cargar el modelo entrenado
with open('c://users//Sergi//proyectos//proyecto_final//models//Modelo_Random_Forest_Base_Completa', 'rb') as f:
    modelo = pickle.load(f)

# Cargar el diccionario de factorización
factorization_dict = pd.read_csv('c://users//Sergi//proyectos//proyecto_final//src//factorization_dict.csv')

# Crear un diccionario de mapeo inverso a partir del diccionario de factorización
inverse_factorization_dict = {col: {str(val): key for key, val in factorization_dict[col].items()} for col in factorization_dict.columns}

st.image('c://users//Sergi//proyectos//logo.jpg', width=100) 

# Título de la aplicación con estilo
st.title(":blue[Tasa y vende tu auto en 1 día]")
st.divider()
st.subheader("Olvídate de la burocracia! Cambia o vende en línea y en menos de 24 hrs", divider='blue')

# Convertir las selecciones del usuario de nuevo a las variables originales
# Convertir las selecciones del usuario de nuevo a las variables originales
manufacturer = st.selectbox('Fabricante', [''] + list(inverse_factorization_dict['manufacturer'].keys()), key='manufacturer')
model_input = st.selectbox('Modelo', [''] + list(inverse_factorization_dict['model'].keys()), key='model')
fuel = st.selectbox('Combustible', [''] + list(inverse_factorization_dict['fuel'].keys()), key='fuel')
transmission = st.selectbox('Transmisión', [''] + list(inverse_factorization_dict['transmission'].keys()), key='transmission')
drive = st.selectbox('Tracción', [''] + list(inverse_factorization_dict['drive'].keys()), key='drive')
size = st.selectbox('Tamaño', [''] + list(inverse_factorization_dict['size'].keys()), key='size')
type_ = st.selectbox('Tipo de Vehículo', [''] + list(inverse_factorization_dict['type'].keys()), key='type')
state = st.selectbox('Estado', [''] + list(inverse_factorization_dict['state'].keys()), key='state')

# Espaciado entre los elementos de entrada y el botón de predicción
st.markdown("---")

# Botón para predecir el precio con un estilo más llamativo
if st.button('Tasar Auto', key='submit_button'):
    # Crear un DataFrame con los datos ingresados
    data = pd.DataFrame({
        'year': [year],
        'manufacturer': [int(inverse_factorization_dict['manufacturer'][manufacturer])],
        'model': [int(inverse_factorization_dict['model'][model_input])],
        'fuel': [int(inverse_factorization_dict['fuel'][fuel])],
        'odometer': [odometer],
        'transmission': [int(inverse_factorization_dict['transmission'][transmission])],
        'drive': [int(inverse_factorization_dict['drive'][drive])],
        'size': [int(inverse_factorization_dict['size'][size])],
        'type': [int(inverse_factorization_dict['type'][type_])],
        'state': [int(inverse_factorization_dict['state'][state])]
    })
    
    # Realizar la predicción
    prediction = modelo.predict(data)
    # Mostrar la oferta estimada con estilo
    st.markdown(f"<h2 style='color: #000000;'>La oferta estimada por tu vehiculo sera: ${prediction[0]:,.2f}</h2>", unsafe_allow_html=True)
