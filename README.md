<p align="center"> 
<img src="https://user-images.githubusercontent.com/69567089/132707858-021aeaf4-8cf9-44e9-b4d3-0350b60418de.png">
</p>

## Índice
- [Conceptos generales](#conceptos-generales)
- [Librería python](#librería-python)
  - [Instalación](#instalación)
  - [Objetos SIMEM](#objetos-simem)
    - [Catalogos de SIMEM.co](#catalogos-de-simemco)
    - [Conjuntos de datos disponibles](#conjuntos-de-datos-disponibles)
    - [¿Cuál conjunto contiene una variable?](#cuál-conjunto-contiene-una-variable)
    - [Ejemplo de uso](#ejemplo-de-uso)
  - [Objetos SINERGOX - XM](#objetos-sinergox---xm)
    - [¿Cómo se pueden consultar el listado de métricas disponibles en la API XM a través de python?](#cómo-se-pueden-consultar-el-listado-de-métricas-disponibles-en-la-api-xm-a-través-de-python)
- [Excel (VBA)](#excel-vba)
  - [SIMEM](#simem)
  - [SINERGOX - XM](#sinergox---xm)
- [Endpoints API](#endpoints-api)
  - [SIMEM](#simem-1)
    - [Restricciones](#restricciones)
    - [Elementos para su uso](#elementos-para-su-uso)
  - [SINERGOX - XM](#sinergox---xm-1)
    - [Restricciones:](#restricciones-1)
    - [Variables disponibles para consumir en la API XM](#variables-disponibles-para-consumir-en-la-api-xm)
    - [¿Cómo realizar solicitudes filtrando por atributos específicos? _(Parámetro opcional)_](#cómo-realizar-solicitudes-filtrando-por-atributos-específicos-parámetro-opcional)
    - [Elementos necesarios para utilizar el servicio desde cualquier cliente](#elementos-necesarios-para-utilizar-el-servicio-desde-cualquier-cliente)
    - [Ejemplo para realizar una petición](#ejemplo-para-realizar-una-petición)


<a id='conceptosGenerales'></a>
# Conceptos generales 
Este repositorio se crea con el fin de compartir herramientas de consulta para extraer información relevante del Mercado de Energía Mayorista colombiano usando las librerías asociadas a las api XM y api SIMEM. A partir de esta guía, el lector estará en capacidad de construir clientes que consuman el servicio utilizando la herramienta de su preferencia: python, excel con VBA o directamente la api.

**Para utilizar la API XM no se requiere gestionar ningún usuario o clave**

El equipo de Analítica ha diseñado herramientas para consumir el servicio en los siguientes lenguajes:

|Lenguaje|Nombre|Tipo|Instalación|Habilidad requerida|
|--------|------|----|-----------|-------------------|
|Python|[pydataxm](https://pypi.org/project/pydataxm/)|Librería| <code> $ pip install pydataxm </code>|Low Code|
|Excel (VBA) | [Consulta_API_SINERGOX_XM.xlsm](https://github.com/EquipoAnaliticaXM/API_XM/tree/master/Consulta_API_SINERGOX_XM.xlsm)|Macro|No Aplica|No Code|
|Excel (VBA) | [Consulta_API_SIMEM.xlsm](https://github.com/EquipoAnaliticaXM/API_XM/tree/master/Consulta_API_SIMEM.xlsm)|Macro|No Aplica|No Code|

# Librería python

> [!WARNING]
> **La librería pydataxm es compatible con versiones superior o iguales a python 3.10.4**

Cada página web de información tiene objetos de python relacionados directamente, se pueden utilizar con la misma librería y realizando los importes correspondientes. 

- [Objetos SIMEM](#objetos-simem)
- [Objetos SINERGOX](#objetos-sinergox---xm)


<a id='instalacion'></a>
## Instalación
  
```console
pip install pydataxm
```

También se puede clonar el repositorio en la ruta de preferencia:
```git
git clone https://github.com/EquipoAnaliticaXM/API_XM.git "C:\Users\Public\Documents"
```


<a id='objSIMEM'></a>
## Objetos SIMEM

**Importación en proyecto**
```python
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM
```
<a id='catalogoDatasets'></a>
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

<a id='catalogovariables'></a>
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



<a id='objSINERGOX'></a>
## Objetos SINERGOX - XM

**Importación en proyecto**
```python
from pydataxm.pydataxm import ReadDB
```

### ¿Cómo se pueden consultar el listado de métricas disponibles en la API XM a través de python?

Para conocer el listado de métricas disponibles se puede consultar el método `get_collections()` como se muestra a continuación:
```python
from pydataxm.pydataxm import ReadDB

# Construir la clase que contiene los métodos de pydataxm
objetoAPI = pydataxm.ReadDB()
objetoAPI.get_collections()
```

# Excel (VBA)
Otra herramienta que se puede utilizar para obtener información de las API disponibles, son los archivos de excel publicados en el repositorio

## SIMEM
En **ListadoVariables** se puede realizar la búsqueda del dataset necesario en relación a la variable; por ejemplo, si se desea conocer la _Demanda real_ voy a tener disponible los conjuntos con **datasetID** _c1b851_ y _b7917_; los cuales se diferencian en la cantidad de desagregaciones disponibles, con uno de estos _ID_ y las fechas para extraer datos se puede realizar la solicitud en la hoja **Princpal**, que además de presentar los datos en la sección inferior, muestra información relacionada al conjunto de datos consultado. 

## SINERGOX - XM
La hoja1 y hoja2 presentan 2 ejemplos de información disponible; la casilla "NombreMetrica" o "Variable" permite elegir entre una lista desplegable los datos que se desean extraer; la única otra opción disponible es la casilla "Filtro" donde se puede realizar un filtrado a través del campo que presenta en "Desagregación". 

> [!IMPORTANT]
> El campo fechas puede ser modificado pero no puede superar los días máximos que condiciona automáticamente cada variable.


# Endpoints API

También se pueden utilizar los enlaces directos con herramientas alternativas a las presentadas en el repositorio usando los enlaces y métodos disponibles.

> [!WARNING]
> Ambas APIs tienen **restricciones** para evitar la congestión del servicio, si se desean utilizar de forma directa, recuerde considerar esta información.

> [!IMPORTANT]
> El formato de fecha que recibe la API es YYYY-MM-DD


## SIMEM

### Restricciones
  Las restricciones existen en relación a la _granularidad_ de cada conjunto de datos. La cantidad de días se mide con la diferencia entre el parámetro _startDate_ y _endDate_.
  - **Catálogos:** No aplica. 
  - **Horaria y Diaria:** Máximo 31 días por llamado
  - **Semanal y Mensual:** Máximo 731 días por llamado
  - **Anual:** Máximo 1827 días por llamado
  

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
- columnDestinyName = Columna por la que se hará filtrado
- values = Lista de valores a filtrar en la columna definida. Separados por "," (coma) si es más de uno.

## SINERGOX - XM

### Restricciones:
Con el fin de no congestionar el servicio, se han establecido restricciones a las consultas así:
* Para datos horarios y diarios, máximo 30 días por llamado
* Para datos mensuales, máximo 731 días por llamado
* Para datos anuales, máximo 366 días por llamado




<a id='section3'></a>
### Variables disponibles para consumir en la API XM

A continuación, se listan las variables que se encuentran disponibles para su consulta, las cuales se encuentran clasificadas por tema:

<details>
<summary>Hidrología</summary>
<ul>
<li> Volumen Útil Diario (Energía) </li>
<li> Volumen Útil Diario por Embalse (Energía) </li>
<li> Aportes Diarios (Energía) </li>
<li> Aportes Diarios por Río (Energía) </li>
<li> Capacidad útil del SIN (Energía) </li>
<li> Capacidad Útil por Embalse (Energía) </li>
<li> Media Histórica de Aportes del SIN (Energía) </li>
<li> Media Histórica de Aportes por Río (Energía) </li>
</ul>
</details>

<details>
<summary>Demanda</summary>
<ul>
<li> Demanda Comercial Total </li>
<li> Demanda Comercial por Agente Comercializador </li>
<li> Demanda del SIN </li>
<li> Demanda por Operador de Red </li>
<li> Perdidas de Energía </li>
<li> Demanda No Atendida Programada por Área </li>
<li> Demanda No Atendida Programada por Subárea </li>
<li> Demanda No Atendida No Programada por Área </li>
<li> Demanda No Atendida No Programada por Subárea </li>
<li> Demanda Comercial Regulada por Agente </li>
<li> Demanda Comercial No regulada por Agente </li>
<li> Demanda Comercial Regulada (Total SIN) </li>
<li> Demanda Comercial No Regulada (Total SIN) </li>
<li> Demanda Comercial No Regulada por CIIU </li>
<li> Demanda Máxima Potencia</li>
<li> Demanda Energía Escenario UPME Alto</li>
<li> Demanda Energía Escenario UPME Medio</li>
<li> Demanda Energía Escenario UPME Bajo</li>
</ul>
</details>

<details>
<summary>Oferta y Generación</summary>
<ul>
<li> Generación Real Total </li>
<li> Generación Real por Recurso (Planta de Generación) </li>
<li> Generación Ideal </li>
<li> Generación Ideal por Recurso (Planta de Generación) </li>
<li> Consumo de Combustible por Recurso (Planta de Generación) </li>
<li> Listado de Recursos de generación con sus principales atributos (Agente Generador, Tipo, Capacidad Efectiva Neta, entre otros) </li>
<li> Generación de Seguridad por Recurso </li>
<li> Generación Fuera de Mérito por Recurso </li>
<li> Obligaciones de Energía Firme por Recurso </li>
<li> Generación Programada Despacho </li>
<li> Generación Programada Redespacho </li>
<li> Disponibilidad Real </li>
<li> Disponibilidad Comercial </li>
<li> Disponibilidad Declarada </li>
<li> Reconciliación Positiva Energía </li>
<li> Reconciliación Negativa Energía </li>
<li> Desviaciones Energía </li>
<li> Compras AGPE </li>
</ul>
</details>

<details>
<summary>Transacciones y Precios</summary>
<ul>
<li> Costo de las Restricciones que se trasladan a la demanda (Restricciones finales) </li>
<li> Precio de Escasez de Activación </li>
<li> Precio de Bolsa Nacional </li>
<li> Máximo Precio de Oferta </li>
<li> Remuneración Real Individual Diaria del Cargo por Confiablidad (RRID) </li>
<li> Precio de Oferta del Despacho </li>
<li> Precio Promedio Contratos Regulado </li>
<li> Precio Promedio Contratos No Regulado </li>
<li> Ventas en Contratos Energía por Agente </li>
<li> Ventas en Contratos Energía (Total SIN) </li>
<li> Compras en Contrato Energía por Agente </li>
<li> Compras en Contrato Energía (Total SIN) </li>
<li> Compras en Bolsa Nacional Energía por Agente </li>
<li> Compras en Bolsa Nacional Energía (Total SIN) </li>
<li> Responsabilidad Comercial AGC </li>
<li> Reconciliación Positiva Moneda </li>
<li> Reconciliación Negativa Moneda </li>
<li> Restricciones sin alivios </li>
<li> Restricciones aliviadas </li>
<li> Desviaciones Moneda </li>
<li> DDV Contratada </li>
<li> FAZNI Moneda </li>
<li> FAER Moneda </li>
<li> PRONE Moneda </li>
<li> MC </li>
<li> Compras Contratos Energía  Mercado Regulado</li>
<li> Compras Contratos Energía  No Mercado Regulado</li>
<li> Rentas de congestión para cubrir restricciones</li>
<li> Saldo Neto TIE Mérito</li>
<li> Saldo Neto TIE Fuera de Mérito</li>
<li> Compras Contratos Energía  Mercado Regulado por Agente</li>
<li> Compras Contratos Energía  No Mercado Regulado por Agente</li>
<li> Precio de Bolsa Nacional TX1</li>
<li> CERE</li>
<li> CEE</li>
<li> Ejecución Garantías</li>
<li> Compras Contratos de Respaldo</li>
<li> Compras Contratos de Respaldo por Recurso</li>
<li> Ventas Contratos de Respaldo</li>
<li> Ventas Contratos de Respaldo por Recurso</li>
<li> Cargos por Uso STN</li>
<li> Cargos por Uso STR</li>
<li> Precio liquidado del Cargo por Confiabilidad</li>
<li> Cargo Máximo T Prima</li>
<li> Cargo Mínimo T Prima</li>
<li> Cargo Media T Prima</li>
<li> Compras Bolsa TIE Moneda Sistema</li>
<li> Compras Bolsa Internacional Moneda Sistema</li>
<li> Compras Bolsa TIE Moneda Agente</li>
<li> Compras Bolsa Internacional Moneda Agente</li>
<li> Ventas Bolsa TIE Moneda Sistema</li>
<li> Ventas Bolsa Internacional Moneda Sistema</li>
<li> Ventas Bolsa TIE Moneda Agente</li>
<li> Ventas Bolsa Internacional Moneda Agente</li> 
</ul>
</details>

<details>
<summary>Intercambios Internacionales</summary>
<ul>
<li> Importaciones en Energía </li>
<li> Exportaciones en Energía </li> 
</ul>
</details>


<details>
<summary>Cálculo de emisiones de CO<sub>2</sub></summary>
<ul>
<li> Emisiones de CO<sub>2</sub> </li>
<li> Emisiones de CH<sub>4</sub> </li>
<li> Emisiones de N<sub>2</sub>O </li>
<li> Emisiones de CO<sub>2</sub>eq </li>
<li> Consumo Combustible Aproximado para el Factor Emisión </li>
<li> Factor de Emisión de la Matriz Energética (CO<sub>2</sub>eq/kWh) </li> 
</ul>
</details>

<details>
<summary>Listados</summary>
<ul>
<li> Listado Recursos con atributos </li>
<li> Listado de agentes con atributos </li>
<li> Listado de métricas </li>
<li> Listado de ríos </li>
<li> Listado de embalses </li>
<li> Listado recursos AGPE</li>
</ul>
</details>

<a id='section4'></a>
### ¿Cómo realizar solicitudes filtrando por atributos específicos? _(Parámetro opcional)_
En caso de no ser especificado dentro de la solicitud, el servicio retornará todos los registros disponibles. 

Con este parámetro se permite extraer datos para una serie de entidades personalizada. Las métricas que pueden ser filtradas son todas aquellas que tienen cruces por:

1. Agente (código SIC del agente _i.e._ CASC, EPMC, ENDG, entre otros)
2. Recurso (código SIC del recurso _i.e._ EPFV, TBST, JEP1, entre otros)
3. Embalse (nombre del embalse _i.e._ EL QUIMBO, GUAVIO, PENOL, entre otros)
4. Río (nombre del río _i.e._ FLORIDA II, BOGOTA N.R., DESV. MANSO, entre otros)

Para conocer el detalle de los códigos SIC de cada recurso o agente le invitamos a consultar las métricas _ListadoRecursos_ y _ListadoAgentes_ disponibles en este mismo servicio.

Para conocer el detalle de los nombres de cada río o embalse le invitamos a consultar las métricas _ListadoRios_ y _ListadoEmbalse_ disponibles en este mismo servicio.

En la carpeta _examples_ encontrará los ejemplos para consumir el servicio usando filtros. [Ir a ejemplos](https://github.com/EquipoAnaliticaXM/API_XM/tree/master/examples)



<a id='section7'></a>
### Elementos necesarios para utilizar el servicio desde cualquier cliente
A continuación, presentamos el listado de métricas disponibles y los parámetros requeridos para realizar peticiones de información:

1. Método: POST
2. Endpoint: 
* https://servapibi.xm.com.co/hourly
* https://servapibi.xm.com.co/daily
* https://servapibi.xm.com.co/monthly
* https://servapibi.xm.com.co/lists
1. Body petición:
```
{"MetricId": "MetricID",
"StartDate": _"YYYY-MM-DD",
"EndDate":_"YYYY-MM-DD",
"Entity": "Cruce",
"Filter":["Listado de codigos"]}
```
> [!NOTE]
> El parámetro _Filter_ es opcional y solo aplica para variables diferente al cruce por _Sistema_


### Ejemplo para realizar una petición

```
POST: https://servapibi.xm.com.co/hourly

Body:
{"MetricId": "Gene",
"StartDate":"2022-09-01",
"EndDate":"2022-09-02",
"Entity": "Recurso",
"Filter":["TBST","GVIO"]}
```
Para conocer el inventario total de variables, cruces y filtros opcionales, consultar:

```
https://servapibi.xm.com.co/lists

Body:
{"MetricId": "ListadoMetricas"}
```


