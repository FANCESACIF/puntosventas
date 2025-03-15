import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image

#avoid warning
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(page_title="Mapa de Agencias FANCESA", layout="wide")


image = Image.open('logo.png')
st.sidebar.image(image, width=150)

st.title("Mapa Comparativo de Agencias FANCESA")

    
# Agregar una línea divisoria
st.markdown("---")

# Cargar datos desde los archivos CSV
agencias_existentes = pd.read_csv('agencias_existentes.csv')
agencias_nuevas = pd.read_csv('agencias_nuevas.csv')

# Agregar columna de tipo
agencias_existentes['tipo'] = 'Existente'
agencias_nuevas['tipo'] = 'Nueva'

# Combinar los dataframes
todas_agencias = pd.concat([agencias_existentes, agencias_nuevas])

# Agregar filtros en la barra lateral
st.sidebar.header("Filtros")

# Filtro por tipo de agencia
tipos_agencias = sorted(todas_agencias['tipo'].unique().tolist())
tipo_seleccionado = st.sidebar.multiselect(
    'Filtrar por Tipo de Agencia',
    tipos_agencias,
    default=tipos_agencias
)

# Filtro por ciudad
ciudades = sorted(todas_agencias['ciudad'].unique().tolist())
ciudad_seleccionada = st.sidebar.multiselect(
    'Filtrar por Ciudad',
    ciudades,
    default=[]
)

# Aplicar filtros
datos_filtrados = todas_agencias.copy()

# Aplicar filtro de tipo de agencia
if tipo_seleccionado:
    datos_filtrados = datos_filtrados[datos_filtrados['tipo'].isin(tipo_seleccionado)]
    st.sidebar.write(f"Mostrando {len(tipo_seleccionado)} tipo(s) de agencia")
else:
    st.sidebar.warning("Por favor, selecciona al menos un tipo de agencia")
    datos_filtrados = pd.DataFrame()  # DataFrame vacío si no hay tipos seleccionados

# Aplicar filtro de ciudad
if ciudad_seleccionada:
    datos_filtrados = datos_filtrados[datos_filtrados['ciudad'].isin(ciudad_seleccionada)]
    st.sidebar.write(f"Mostrando {len(ciudad_seleccionada)} ciudad(es)")
else:
    st.sidebar.info("Mostrando todas las ciudades")

# Agregar control de zoom después de los filtros
st.sidebar.header("Control de Zoom")

# Slider para controlar el zoom del mapa
zoom_level = st.sidebar.slider(
    "Nivel de Zoom del Mapa",
    min_value=3,
    max_value=15,
    value=5,
    help="Desliza para ajustar el nivel de zoom del mapa"
)

# Agregar texto explicativo sobre el uso del zoom
st.sidebar.markdown("""
**Cómo usar el zoom:**
- Valores bajos (3-5): Vista general de Bolivia
- Valores medios (6-10): Vista de departamentos o regiones
- Valores altos (11-15): Vista detallada de ciudades
- También puedes hacer zoom con la rueda del mouse directamente en el mapa
""")

# Verificar si hay datos para mostrar
if datos_filtrados.empty:
    st.warning("No hay datos para mostrar con los filtros seleccionados. Por favor, ajusta los filtros.")
else:
    # Crear el mapa con los datos filtrados
    fig = px.scatter_mapbox(datos_filtrados,
                           lat='latitud',
                           lon='longitud',
                           hover_name='nombre_agencia',
                           hover_data=['ciudad'],
                           color='tipo',
                           text='nombre_agencia',
                           color_discrete_map={'Existente': 'blue', 'Nueva': '#19ED01'},
                           zoom=zoom_level,  # Usar el valor del slider
                           title='Distribución de Agencias en Bolivia')

    # Actualizar el diseño del mapa
    fig.update_layout(
        mapbox_style='open-street-map',  # Cambiado para mejor visualización
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=700,
        mapbox=dict(
            center=dict(
                lat=datos_filtrados['latitud'].mean(),
                lon=datos_filtrados['longitud'].mean()
            ),
            zoom=zoom_level if len(ciudad_seleccionada) != 1 else zoom_level  # Usar el valor del slider
        )
    )

    # Configurar las etiquetas
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10, color='black'),
        marker=dict(size=12)  # Aumentado para mejor visibilidad
    )

    # Mostrar el mapa en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Agregar leyenda explicativa
    st.markdown("""
    ### Leyenda:
    - 🔵 **Agencias Existentes**: Puntos de venta actuales de FANCESA
    - 🟢 **Agencias Nuevas**: Nuevas ubicaciones propuestas
    """)

    # Mostrar estadísticas basadas en los datos filtrados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Agencias Existentes", 
                len(datos_filtrados[datos_filtrados['tipo'] == 'Existente']))
    with col2:
        st.metric("Total Agencias Nuevas", 
                len(datos_filtrados[datos_filtrados['tipo'] == 'Nueva']))
    with col3:
        st.metric("Total Agencias", len(datos_filtrados))

    # Mostrar datos en forma de tabla
    st.subheader("Datos de las Agencias")
    st.dataframe(
        datos_filtrados.sort_values(['ciudad', 'nombre_agencia']),
        hide_index=True
    )

# Agregar información adicional
st.sidebar.header("Información")
st.sidebar.write("""
Esta aplicación muestra la distribución geográfica de las agencias FANCESA,
diferenciando entre las agencias existentes y las nuevas propuestas.
""")
