# PyDataSIMEM 
![Logo SIMEM](/assets/SIMEM_logo_3.png?raw=true)

## Qué es?
Este repositorio se crea con el fin de compartir una herramienta de consulta para extraer información relevante del Mercado de Energía Mayorista colombiano usando la api SIMEM. A partir de esta guía, el lector estará en capacidad de construir clientes que consuman el servicio utilizando la herramienta de su preferencia: python, excel con VBA o directamente la api.

## Generar documentación detallada

Además de este archivo README, es posible generar un archivo html donde se explica con más profundidad todas las clases y funcionalidades que se pueden encontrar dentro de pydatasimem. Para generarlo se deben seguir los siguientes pasos:

1. Clonar el repositorio

```bash
git clone https://github.com/XM-SA-ESP/GEDeN-SIMEM-Tools.git
```

2. Instalar librerías

```bash
pip install sphinx
pip install sphinx_rtd_theme
```

3. Generar documentación

```bash
sphinx-build -b html docs/source docs/_build/html
```

4. Abrir documentación

```bash
start docs\_build\html\index.html
```

### Funcionalidades/Features:

1. Descargar datos desde el SIMEM utilizando python
2. Consolidar diferentes fechas sin necesidad de detenerse por las restricciones del API
3. Ser un puente para integraciones con otros productos de datos basados en información del Mercado de Energía Mayorista

## Índice
- [PyDataSIMEM](#pydatasimem)
  - [Qué es?](#qué-es)
  - [Generar documentación detallada](#generar-documentación-detallada)
    - [Funcionalidades/Features:](#funcionalidadesfeatures)
  - [Índice](#índice)
- [Librería python](#librería-python)
  - [Instalación](#instalación)
    - [Catalogos de SIMEM.co](#catalogos-de-simemco)
    - [Conjuntos de datos disponibles](#conjuntos-de-datos-disponibles)
    - [¿Cuál conjunto contiene una variable?](#cuál-conjunto-contiene-una-variable)
    - [Ejemplo de uso](#ejemplo-de-uso)
- [Excel (VBA)](#excel-vba)
- [Endpoint API](#endpoint-api)
    - [Restricciones](#restricciones)
    - [Documentación API](#documentación-api)
    - [Elementos para su uso](#elementos-para-su-uso)



**Para utilizar la API no se requiere gestionar ningún usuario o clave**

El equipo de Analítica ha diseñado herramientas para consumir el servicio en los siguientes lenguajes:

|Lenguaje|Nombre|Tipo|Instalación|Habilidad requerida|
|--------|------|----|-----------|-------------------|
|Python|[pydataxm](https://pypi.org/project/pydataxm/)|Librería| <code> $ pip install pydataxm </code>|Low Code|
|Excel (VBA) | [Consulta_API_SIMEM.xlsm](https://github.com/EquipoAnaliticaXM/API_XM/tree/master/Consulta_API_SIMEM.xlsm)|Macro|No Aplica|No Code|

# Librería python

> [!WARNING]
> **La librería pydataxm es compatible con versiones superior o iguales a python 3.10.4**

Cada página web de información tiene objetos de python relacionados directamente, se pueden utilizar con la misma librería y realizando los importes correspondientes. 

<a id='instalacion'></a>
## Instalación
  
```console
pip install pydataxm
```

También se puede clonar el repositorio en la ruta de preferencia:
```git
git clone https://github.com/EquipoAnaliticaXM/API_XM.git "C:\Users\Public\Documents"
```


**Importación en proyecto**
```python
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM, VariableSIMEM, MaestraSIMEM
```
### Catalogos de SIMEM.co

> [!IMPORTANT]
> El objeto de los catálogos funciona diferente al objeto de lectura de conjuntos de datos.

Se puede solicitar la información utilizando el objeto asociado a los catálogos de la página. Instanciar la clase guarda toda la información en atributos que pueden leerse utilizando las funciones `.get_atributo`

### Conjuntos de datos disponibles
```python
# Importación
from pydataxm.pydatasimem import CatalogSIMEM

# Crear una instancia de catalogo con el tipo
catalogo_conjuntos = CatalogSIMEM('Datasets')

# Extraer información a utilizar
print("Nombre: ", catalogo_conjuntos.get_name())
print("Metadata: ", catalogo_conjuntos.get_metadata())
print("Columnas: ", catalogo_conjuntos.get_columns())

#  Dataframe con información de los conjuntos de datos
data = catalogo_conjuntos.get_data()
print(data)
```

Para obtener las variableas y maestras disponibles dentro de las clases de VariableSIMEM y MaestraSIMEM, se utilizan las siguientes funciones

```python
# Importación
from pydataxm.pydatasimem import VariableSIMEM, MaestraSIMEM

# Obtener listado de variables disponibles
catalogo_variables = VariableSIMEM.get_collection()

print(catalogo_variables)

# Obtener listado de maestras disponibles
catalogo_maestras = MaestraSIMEM.get_collection()

print(catalogo_maestras)


### ¿Cuál conjunto contiene una variable?

```python
# Importación
from pydataxm.pydatasimem import CatalogSIMEM

# Crear una instancia de catalogo con el tipo
catalogo_vbles = CatalogSIMEM('variables')

# Extraer información a utilizar
print("Nombre: ", catalogo_vbles.get_name())
print("Metadata: ", catalogo_vbles.get_metadata())
print("Columnas: ", catalogo_vbles.get_columns())

# Dataframe con información de las variables
data = catalogo_vbles.get_data()
print(data)
```

### Ejemplo de uso
> [!NOTE]
> La ejecución del snippet con las fechas definidas tarda entre 1 y 2 minutos en ejecutar completamente. Se recomienda usar un cuaderno Jupyter similar a los [ejemplos](https://github.com/EquipoAnaliticaXM/API_XM/tree/master/examples).

El siguiente snippet busca el conjunto asociado a la generación real y realiza una consulta para unas fechas arbitrarias sin el uso de los filtros.
```python
# Importación
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM

# Buscar el id del conjunto de datos
catalogo = CatalogSIMEM('Datasets')
data_catalogo = catalogo.get_data()
print(data_catalogo.query("nombreConjuntoDatos.str.contains('Generación Real')"))

# Crear una instancia de ReadSIMEM
dataset_id = 'E17D25'
fecha_inicio = '2024-04-01'
fecha_fin = '2024-04-30'
generacion = ReadSIMEM(dataset_id, fecha_inicio, fecha_fin)

# Recuperar datos
data = generacion.main(filter=False)
print(data)
```

# Excel (VBA)

En **ListadoVariables** se puede realizar la búsqueda del dataset necesario en relación a la variable; por ejemplo, si se desea conocer la _Demanda real_ voy a tener disponible los conjuntos con **datasetID** _c1b851_ y _b7917_; los cuales se diferencian en la cantidad de desagregaciones disponibles, con uno de estos _ID_ y las fechas para extraer datos se puede realizar la solicitud en la hoja **Princpal**, que además de presentar los datos en la sección inferior, muestra información relacionada al conjunto de datos consultado. 


# Endpoint API

También se pueden utilizar los enlaces directos con herramientas alternativas a las presentadas en el repositorio usando los enlaces y métodos disponibles.

> [!WARNING]
> Ambas APIs tienen **restricciones** para evitar la congestión del servicio, si se desean utilizar de forma directa, recuerde considerar esta información.

> [!IMPORTANT]
> El formato de fecha que recibe la API es YYYY-MM-DD



### Restricciones
  Las restricciones existen en relación a la _granularidad_ de cada conjunto de datos. La cantidad de días se mide con la diferencia entre el parámetro _startDate_ y _endDate_.
  - **Catálogos:** No aplica. 
  - **Horaria y Diaria:** Máximo 31 días por llamado
  - **Semanal y Mensual:** Máximo 731 días por llamado
  - **Anual:** Máximo 1827 días por llamado
  

### Documentación API
También se puede realizar la consulta utilizando directamente la API. Descarga la [documentación](https://www.simem.co/recursos/Documentacion%20API%20SIMEM.pdf) para ver los ejemplos


### Elementos para su uso
Se utiliza el método GET para traer la información utilizando el siguiente **enlace:**

>[!IMPORTANT]
> El parámetro **datasetid** es obligatorio para cualquier consulta.
```
https://www.simem.co/backend-files/api/PublicData?datasetid={}
```

**Parámetros:**
- datasetId = Código único de 6 dígitos alfanuméricos que representa el conjunto de datos a consultar
- startDate = Fecha del primer dato
- endDate = Fecha del último dato
- filters = Filtros que se usaran
