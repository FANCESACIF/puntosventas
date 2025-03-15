# FANCESA Puntos de Venta

## Descripción
Esta aplicación web permite visualizar y comparar la distribución geográfica de los puntos de venta de FANCESA (Fábrica Nacional de Cemento S.A.), diferenciando entre agencias existentes y nuevas propuestas. La herramienta facilita la toma de decisiones para la expansión de la red de distribución mediante georeferenciación.

## Características
- **Mapa interactivo**: Visualización de todas las agencias en un mapa interactivo de Bolivia
- **Filtros dinámicos**: Posibilidad de filtrar por:
  - Tipo de agencia (Existente/Nueva)
  - Ciudad
- **Control de zoom**: Ajuste del nivel de detalle del mapa
- **Estadísticas**: Métricas sobre el número de agencias por categoría
- **Tabla de datos**: Visualización tabular de la información de las agencias

## Requisitos
- Python 3.6+
- Streamlit
- Pandas
- Plotly
- Pillow (PIL)

## Instalación

1. Clonar el repositorio:
```
git clone https://github.com/su-usuario/puntosventas.git
cd puntosventas
```

2. Instalar las dependencias:
```
pip install -r requirements.txt
```

## Uso

1. Preparar los archivos de datos:
   - `agencias_existentes.csv`: Datos de las agencias actuales
   - `agencias_nuevas.csv`: Datos de las nuevas propuestas
   - `logo.png`: Logo de FANCESA

2. Ejecutar la aplicación:
```
streamlit run comparativa_geo_agencias.py
```

3. Acceder a la aplicación web en su navegador (generalmente en http://localhost:8501)

## Estructura de los archivos CSV

Los archivos CSV deben contener al menos las siguientes columnas:
- `nombre_agencia`: Nombre del punto de venta
- `ciudad`: Ciudad donde se ubica
- `latitud`: Coordenada geográfica (latitud)
- `longitud`: Coordenada geográfica (longitud)

## Contribución
Para contribuir a este proyecto, por favor:
1. Haga un fork del repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realice sus cambios y haga commit (`git commit -am 'Añadir nueva funcionalidad'`)
4. Envíe los cambios a su fork (`git push origin feature/nueva-funcionalidad`)
5. Cree un Pull Request
