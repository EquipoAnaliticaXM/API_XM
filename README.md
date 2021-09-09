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
Este repositorio se crea con el fin de compartir herramientas de consulta para extraer información relevante del Mercado de Energía Mayorista colombiano. A partir de esta guía, el lector estará en capacidad de construir clientes que consuman el servicio utilizando la herramienta de su preferencia. Posteriormente, detallaremos dos aproximaciones utilizando VBA y Python

<a id='section2'></a>
## Variables disponibles para consumir en la API XM

A continuación, se listan las variables que se encuentran disponibles para su consulta, las cuales se encuentran clasificadas por tema:

<details>
<summary>Hidrología</summary>
<ul>
<li> Volumen Útil Diario (Energía) [kWh] </li>
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
</ul>
</details>

<a id='section3'></a>
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

Para conocer el detalle de los códigos (bdMEM) de cada recurso o agente le invitamos a consultar las métricas _ListadoRecursos_ y _ListadoAgentes_ disponibles en este mismo servicio.

Para conocer el detalle de los nombres de cada río o embalse le invitamos a consultar las métricas _ListadoRios_ y _ListadoEmbalse_ disponibles en este mismo servicio.

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
A continuación, presentamos el listado de métricas disponibles y los parámetros requeridos para realizar peticiones de información.
| Nombre de variable                                                    | Unidad de medida | Granularidad | Parámetros                                                                                                | URL                                |
|-----------------------------------------------------------------------|------------------|--------------|-----------------------------------------------------------------------------------------------------------|------------------------------------|
| Consumo Combustible Recursos pertenecientes al Despacho Central       | MBTU             | Horaria      | {"MetricId": "ConsCombustibleMBTU","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Recurso"}  | http://servapibi.xm.com.co/hourly  |
| Generación Real por recurso                                           | kWh              | Horaria      | {"MetricId": "Gene","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Recurso"}                 | http://servapibi.xm.com.co/hourly  |
| Generación Real (Total SIN)                                           | kWh              | Horaria      | {"MetricId": "Gene","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}                 | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial por Agente                                          | kWh              | Horaria      | {"MetricId": "DemaCome","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Agente"}              | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial (Total SIN)                                         | kWh              | Horaria      | {"MetricId": "DemaCome","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}             | http://servapibi.xm.com.co/hourly  |
| Precio de Oferta del Despacho                                         | $COP/kWh         | Horaria      | {"MetricId": "PrecOferDesp","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Recurso"}         | http://servapibi.xm.com.co/hourly  |
| Precio de Bolsa Nacional                                              | $COP/kWh         | Horaria      | {"MetricId": "PrecBolsNaci","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}         | http://servapibi.xm.com.co/hourly  |
| Máximo Precio de Oferta Nacional                                      | $COP/kWh         | Horaria      | {"MetricId": "MaxPrecOferNal","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}       | http://servapibi.xm.com.co/hourly  |
| Precio de Escasez de Activación                                       | $COP/kWh         | Diaria       | {"MetricId": "PrecEscaAct","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}          | http://servapibi.xm.com.co/daily   |
| Restricciones Aliviadas (Total SIN)                                   | $COP             | Horaria      | {"MetricId": "RestAliv","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}             | http://servapibi.xm.com.co/hourly  |
| Generación Ideal                                                      | kWh              | Horaria      | {"MetricId": "GeneIdea","StartDate": "2018-01-01","EndDate": "2018-01-01","Entity":"Sistema"}             | http://servapibi.xm.com.co/hourly  |
| Volumen Útil en Energía                                               | kWh              | Diaria       | {"MetricId": "VoluUtilDiarEner","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Sistema"}     | http://servapibi.xm.com.co/daily   |
| Volumen Útil en Energía por Embalse                                   | kWh              | Diaria       | {"MetricId": "VoluUtilDiarEner","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Embalse"}     | http://servapibi.xm.com.co/daily   |
| Aportes Energía                                                       | kWh              | Diaria       | {"MetricId": "AporEner","StartDate": "2019-01-01","EndDate": "2019-01-31","Entity":"Sistema"}             | http://servapibi.xm.com.co/daily   |
| Aportes Energía por Rio                                               | kWh              | Diaria       | {"MetricId": "AporEner","StartDate": "2019-01-01","EndDate": "2019-01-31","Entity":"Rio"}                 | http://servapibi.xm.com.co/daily   |
| Capacidad Útil                                                        | kWh              | Diaria       | {"MetricId": "CapaUtilDiarEner","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Sistema"}     | http://servapibi.xm.com.co/daily   |
| Capacidad Útil por Embalse                                            | kWh              | Diaria       | {"MetricId": "CapaUtilDiarEner","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Embalse"}     | http://servapibi.xm.com.co/daily   |
| Media Histórica de Aportes                                            | kWh              | Diaria       | {"MetricId": "AporEnerMediHist","StartDate": "2019-01-01","EndDate": "2019-01-31","Entity":"Sistema"}     | http://servapibi.xm.com.co/daily   |
| Media Histórica de Aportes por Río                                    | kWh              | Diaria       | {"MetricId": "AporEnerMediHist","StartDate": "2019-01-01","EndDate": "2019-01-31","Entity":"Rio"}         | http://servapibi.xm.com.co/daily   |
| Remuneración Real Individual Diaria del Cargo por Confiabilidad– RRID | $COP             | Diaria       | {"MetricId": "RemuRealIndiv","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Sistema"}        | http://servapibi.xm.com.co/daily   |
| Generación Ideal por Recurso                                          | kWh              | Horaria      | {"MetricId": "GeneIdea", "StartDate": "2015-01-01", "EndDate": "2015-01-31", "Entity" : "Recurso"}        | http://servapibi.xm.com.co/hourly  |
| Precio Promedio Contratos Regulado                                    | $COP/kWh         | Horaria       | {"MetricId": "PrecPromContRegu", "StartDate": "2015-01-01",EndDate": "2015-01-31","Entity" : "Sistema"}   | http://servapibi.xm.com.co/hourly   |
| Precio Promedio Contratos No Regulado                                 | $COP/kWh         | Horaria       | {"MetricId": "PrecPromContNoRegu", "StartDate": "2015-01-01",EndDate": "2015-01-31","Entity" : "Sistema"} | http://servapibi.xm.com.co/hourly   |
| Ventas en Contratos Energía por Agente                                | kWh              | Horaria      | {"MetricId": "VentContEner","StartDate": "2015-01-01","EndDate": "2015-01-31","Entity" : "Agente"}        | http://servapibi.xm.com.co/hourly  |
| Ventas en Contratos Energía (Total SIN)                               | kWh              | Horaria      | {"MetricId": "VentContEner","StartDate": "2015-01-01","EndDate": "2015-01-31","Entity" : "Sistema"}       | http://servapibi.xm.com.co/hourly  |
| Compras en Contrato Energía por Agente                                | kWh              | Horaria      | {"MetricId": "CompContEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}       | http://servapibi.xm.com.co/hourly  |
| Compras en Contrato Energía (Total SIN)                               | kWh              | Horaria      | {"MetricId": "CompContEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}      | http://servapibi.xm.com.co/hourly  |
| Compras en Bolsa Nacional Energía por Agente                          | kWh              | Horaria      | {"MetricId": "CompBolsNaciEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}   | http://servapibi.xm.com.co/hourly  |
| Compras en Bolsa Nacional Energía (Total SIN)                         | kWh              | Horaria      | {"MetricId": "CompBolsNaciEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}  | http://servapibi.xm.com.co/hourly  |
| Consumo Combustible Aproximado para Factor de Emisión                 | MBTU             | Horaria      | {"MetricId": "ConsCombAprox","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "RecursoComb"} | http://servapibi.xm.com.co/hourly  |
| Emisiones CO2                                                         | Toneladas        | Horaria      | {"MetricId": "EmisionesCO2","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "RecursoComb"}  | http://servapibi.xm.com.co/hourly  |
| Emisiones CH4                                                         | Toneladas        | Horaria      | {"MetricId": "EmisionesCH4","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "RecursoComb"}  | http://servapibi.xm.com.co/hourly  |
| Emisiones N2O                                                         | Toneladas        | Horaria      | {"MetricId": "EmisionesN2O","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "RecursoComb"}  | http://servapibi.xm.com.co/hourly  |
| Emisiones CO2e                                                        | Toneladas        | Horaria      | {"MetricId": "EmisionesCO2Eq","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}    | http://servapibi.xm.com.co/hourly  |
| Factor Emision SIN                                                    | g/kWh            | Horaria      | {"MetricId": "factorEmisionCO2e","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"} | http://servapibi.xm.com.co/hourly  |
| Importaciones Energía                                                 | kWh              | Horaria      | {"MetricId": "ImpoEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}          | http://servapibi.xm.com.co/hourly  |
| Demanda por OR                                                        | kWh              | Horaria      | {"MetricId": "DemaOR","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}             | http://servapibi.xm.com.co/hourly  |
| Perdidas de Energía                                                   | kWh              | Horaria      | {"MetricId": "PerdidasEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}      | http://servapibi.xm.com.co/hourly  |
| Demanda del SIN                                                       | kWh              | Diaria       | {"MetricId": "DemaSIN","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}           | http://servapibi.xm.com.co/daily   |
| Demanda No Atendida Programada por Area                               | kWh              | Diaria       | {"MetricId": "DemaNoAtenProg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Area"}       | http://servapibi.xm.com.co/daily   |
| Demanda No Atendida Programada por Subarea                            | kWh              | Diaria       | {"MetricId": "DemaNoAtenProg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Subarea"}    | http://servapibi.xm.com.co/daily   |
| Demanda No Atendida No Programada por Area                            | kWh              | Diaria       | {"MetricId": "DemaNoAtenNoProg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Area"}     | http://servapibi.xm.com.co/daily   |
| Demanda No Atendida No Programada por Subarea                         | kWh              | Diaria       | {"MetricId": "DemaNoAtenNoProg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Subarea"}  | http://servapibi.xm.com.co/daily   |
| Generación de Seguridad por Recurso                                   | kWh              | Horaria      | {"MetricId": "GeneFueraMerito","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}   | http://servapibi.xm.com.co/hourly  |
| Generación Fuera de Mérito por Recurso                                | kWh              | Horaria      | {"MetricId": "PerdidasEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}      | http://servapibi.xm.com.co/hourly  |
| Obligaciones de Energía Firme por Recurso                             | kWh              | Diaria      | {"MetricId": "ObligEnerFirme","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}    | http://servapibi.xm.com.co/hourly  |
| FAZNI                                                                 | kWh              | Diaria       | {"MetricId": "FAZNI","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}             | http://servapibi.xm.com.co/daily   |
| FAER                                                                  | kWh              | Mensual      | {"MetricId": "FAER","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}              | http://servapibi.xm.com.co/monthly |
| PRONE                                                                 | kWh              | Mensual      | {"MetricId": "PRONE","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}             | http://servapibi.xm.com.co/monthly |
| Exportaciones Energia                                                 | kWh              | Horaria      | {"MetricId": "ExpoEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}          | http://servapibi.xm.com.co/hourly  |
| Generación Programada Despacho                                        | kWh              | Horaria      | {"MetricId": "GeneProgDesp","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}      | http://servapibi.xm.com.co/hourly  |
| Generación Programada Redespacho                                      | kWh              | Horaria      | {"MetricId": "GeneProgRedesp","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}     | http://servapibi.xm.com.co/hourly  |
| Disponibilidad Real                                                   | kWh              | Horaria      | {"MetricId": "DispoReal","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}         | http://servapibi.xm.com.co/hourly  |
| Disponibilidad Comercial                                              | kWh              | Horaria      | {"MetricId": "DispoCome","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}         | http://servapibi.xm.com.co/hourly  |
| Disponibilidad Declarada                                              | kWh              | Horaria      | {"MetricId": "DispoDeclarada","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}    | http://servapibi.xm.com.co/hourly  |
| DDV Contratatada                                                      | kWh              | Diaria       | {"MetricId": "DDVContratada","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}     | http://servapibi.xm.com.co/daily   |
| Reconciliación Positiva Energía                                       | kWh              | Horaria      | {"MetricId": "RecoPosEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}       | http://servapibi.xm.com.co/hourly  |
| Reconciliación Negativa Energía                                       | kWh              | Horaria      | {"MetricId": "RecoNegEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}       | http://servapibi.xm.com.co/hourly  |
| Responsabilidad Comercial AGC                                         | $COP             | Horaria      | {"MetricId": "RespComerAGC","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}       | http://servapibi.xm.com.co/hourly  |
| Desviaciones Energía                                                  | kWh              | Horaria      | {"MetricId": "DesvEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}          | http://servapibi.xm.com.co/hourly  |
| Desviaciones Moneda                                                   | $COP             | Horaria      | {"MetricId": "DesvMoneda","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}        | http://servapibi.xm.com.co/hourly  |
| Reconciliación Positiva Moneda                                        | $COP             | Horaria      | {"MetricId": "RecoPosMoneda","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}     | http://servapibi.xm.com.co/hourly  |
| Reconciliación Negativa Moneda                                        | $COP             | Horaria      | {"MetricId": "RecoNegMoneda","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Recurso"}     | http://servapibi.xm.com.co/hourly  |
| Compras AGPE                                                          | kWh              | Horaria      | {"MetricId": "ExcedenteAGPE","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}      | http://servapibi.xm.com.co/hourly  |
| MC                                                                    | $COP/kWh         | Mensual      | {"MetricId": "MC","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}                | http://servapibi.xm.com.co/monthly |
| Demanda Comercial Regulada por Agente                                 | kWh              | Horaria      | {"MetricId": "DemaComeReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}       | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial No regulada por Agente                              | kWh              | Horaria      | {"MetricId": "DemaComeNoReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}      | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial Regulada (Total SIN)                                | kWh              | Horaria      | {"MetricId": "DemaComeReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}        | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial No Regulada (Total SIN)                             | kWh              | Horaria      | {"MetricId": "DemaComeNoReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}     | http://servapibi.xm.com.co/hourly  |
| Restricciones sin alivios                                             | $COP             | Horaria      | {"MetricId": "RestSinAliv","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}       | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial No Regulada por CIIU                                | kWh              | Horaria      | {"MetricId": "DemaComeNoReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "CIIU"}        | http://servapibi.xm.com.co/hourly  |
| Listado Recursos con atributos                                        | NA               | Lista        | {"MetricId": "ListadoRecursos","Entity" : "Sistema"}                                                      | http://servapibi.xm.com.co/lists   |
| Listado de agentes con atributos                                      | NA               | Lista        | {"MetricId": "ListadoAgentes" ,"Entity" : "Sistema"}                                                      | http://servapibi.xm.com.co/lists   |
