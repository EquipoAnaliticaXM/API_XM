<p align="center"> 
<img src="https://user-images.githubusercontent.com/69567089/132707858-021aeaf4-8cf9-44e9-b4d3-0350b60418de.png">
</p>

## Índice
1. [Conceptos generales de la API XM](#section1)
2. [Variables disponibles para consumir en la API XM](#section2)
3. [Soluciones diseñadas para consumir la API](#section3)
4. [Cómo realizar solicitudes filtrando por atributos específicos\?](#section4)
5. [Restricciones de la API](#section5)
6. [Comentarios finales](#section6)
7. [Elementos necesarios para utilizar el servicio desde cualquier cliente](#section7)

<a id='section1'></a>
## Conceptos generales de la API XM
Este repositorio se crea con el fin de compartir herramientas de consulta para extraer información relevante del Mercado de Energía Mayorista colombiano usando la API XM. A partir de esta guía, el lector estará en capacidad de construir clientes que consuman el servicio utilizando la herramienta de su preferencia. Posteriormente, detallaremos dos aproximaciones utilizando VBA y Python.

**Para utilizar la API XM no se requiere gestionar ningún usuario o clave**

<a id='section2'></a>
## ¿Cómo se pueden consultar el listado de métricas disponibles en la API XM a través de códido? 
Para conocer el listado de métricas disponibles se puede consultar el método get_collections() como se muestra a continuación:
1. from pydataxm import *          # Importa la libreria que fue instalada con pip install pydataxm o tambien desde GitHub
2. objetoAPI = pydataxm.ReadDB()     # Construir la clase que contiene los métodos de pydataxm
3. objetoAPI.get_collections()

<a id='section3'></a>
## Variables disponibles para consumir en la API XM

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
## Soluciones diseñadas para consumir la API

Tal como se indicó al inicio, el equipo de Analítica ha diseñado dos aproximaciones para consumir el servicio en los siguientes lenguajes:

|Lenguaje|Nombre|Tipo|Instalación|Habilidad requerida|
|--------|------|----|-----------|-------------------|
|Python|pydataxm|Librería| <code> $ pip install pydataxm </code>|Low Code|
|Excel (VBA) | Consulta_API_XM.xlsm|Macro|No Aplica|No Code|

<a id='section4'></a>
## ¿Cómo realizar solicitudes filtrando por atributos específicos? _(Parámetro opcional)_
En caso de no ser especificado dentro de la solicitud, el servicio retornará todos los registros disponibles. 

Con este parámetro se permite extraer datos para una serie de entidades personalizada. Las métricas que pueden ser filtradas son todas aquellas que tienen cruces por:

1. Agente (código SIC del agente _i.e._ CASC, EPMC, ENDG, entre otros)
2. Recurso (código SIC del recurso _i.e._ EPFV, TBST, JEP1, entre otros)
3. Embalse (nombre del embalse _i.e._ EL QUIMBO, GUAVIO, PENOL, entre otros)
4. Río (nombre del río _i.e._ FLORIDA II, BOGOTA N.R., DESV. MANSO, entre otros)

Para conocer el detalle de los códigos SIC de cada recurso o agente le invitamos a consultar las métricas _ListadoRecursos_ y _ListadoAgentes_ disponibles en este mismo servicio.

Para conocer el detalle de los nombres de cada río o embalse le invitamos a consultar las métricas _ListadoRios_ y _ListadoEmbalse_ disponibles en este mismo servicio.

En la carpeta _examples_ encontrará los ejemplos para consumir el servicio usando filtros. [Ir a ejemplos](https://github.com/EquipoAnaliticaXM/API_XM/tree/master/examples)

<a id='section5'></a>
## Restricciones de la API:
Con el fin de no congestionar el servicio, se han establecido restricciones a las consultas así:
* Para datos horarios y diarios, máximo 30 días por llamado
* Para datos mensuales, máximo 731 días por llamado
* Para datos anuales, máximo 366 días por llamado

<a id='section6'></a>
## Comentarios finales
Tener en cuenta que el formato de fecha que recibe la API es YYYY-MM-DD

<a id='section7'></a>
## Elementos necesarios para utilizar el servicio desde cualquier cliente
A continuación, presentamos el listado de métricas disponibles y los parámetros requeridos para realizar peticiones de información:

1. Método: POST
2. Endpoint: 
* https://servapibi.xm.com.co/hourly
* https://servapibi.xm.com.co/daily
* https://servapibi.xm.com.co/monthly
* https://servapibi.xm.com.co/lists
3. Body petición:
```
{"MetricId": "MetricID",
"StartDate": _"YYYY-MM-DD",
"EndDate":_"YYYY-MM-DD",
"Entity": "Cruce",
"Filter":["Listado de codigos"]}
```
**Nota:** El parámetro _Filter_ es opcional y solo aplica para variables diferente al cruce por _Sistema_
## Ejemplo para realizar una petición

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
