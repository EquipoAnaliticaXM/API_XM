# Conceptos generales de la API XM
Este repositorio se crea con el fin de compartir herramientas de consulta para extraer información relevante del Mercado de Energía Mayorista colombiano, a partir de esta guía, el lector estará en capacidad de construir clientes que consuman el servicio utilizando la herramienta de su preferencia. Posteriormente, detallaremos dos aproximaciones utilizando VBA y Python

## Variables disponibles para consumir en la API XM

A continuacion se listan las variables que se encuentran disponibles para su consulta, las cuales se encuentran clasificadas por tema:

### Hidrología
* Volumen Útil Diario (Energía)
* Volumen Útil Diario por Embalse (Energía)
* Aportes Diarios (Energía)
* Aportes Diarios por Río (Energía)
* Capacidad útil del SIN (Energía)
* Capacidad Útil por Embalse (Energía)
* Media Historica de Aportes del SIN (Energía)
* Media Historica de Aportes por Río (Energía)
### Demanda
* Demanda Comercial Total
* Demanda Comercial por Agente Comercializador
* Demanda del SIN
* Demanda por Operador de Red
* Perdidas de Energía
* Demanda No Atendida Programada por Área
* Demanda No Atendida Programada por Subárea
* Demanda No Atendida No Programada por Área
* Demanda No Atendida No Programada por Subárea
### Oferta y Generación
* Generación Real Total 
* Generación Real por Recurso (Planta de Generación)
* Generación Ideal
* Generación Ideal por Recurso (Planta de Generación)
* Consumo de Combustible por Recurso (Planta de Generación)
* Listado de Rcursos de generación con sus principales atributos (Agente Generador, Tipo, Capacidad Efectiva Neta, entre otros)
* Generación de Seguridad por Recurso
* Generación Fuera de Mérito por Recurso
* Obligaciones de Energía Firme por Recurso
### Transacciones y Precios
* Costo de las Restricciones que se trasladan a la demanda (Restricciones finales)
* Precio de Escasez de Activación
* Precio de Bolsa Nacional
* Máximo Precio de Oferta
* Remuneración Real Individual Diaria del Cargo por Confiablidad (RRID)
* Precio de Oferta del Despacho
*  Precio Promedio Contratos Regulado
* Precio Promedio Contratos No Regulado
* Ventas en Contratos Energía por Agente
* Ventas en Contratos Energía (Total SIN)
* Compras en Contrato Energía por Agente
* Compras en Contrato Energía (Total SIN)
* Compras en Bolsa Nacional Energía por Agente
* Compras en Bolsa Nacional Energía (Total SIN)
* FAZNI Moneda
* FAER Moneda
* PRONE Moneda
#### Intercambios Internacionales
* Importaciones en Energía
### Cálculo de emisiones de CO2
* Emisiones de CO2
* Emisiones de CH4
* Emisiones de N2O
* Emisiones de CO2eq
* Consumo Combustible Aproximado para el Factor Emisión
* Factor de Emisión de la Matriz Energética (CO2eq/kWh)


## Restricciones de la API:
Con el fin de evitar saturar el servicio, se han establecido restricciones a las consultas así:
* Para datos horarios y diarios, máximo 30 días por llamado
* Para datos anuales, máximo 366 días por llamado
* Para el Listado de Recursos de Generación el limite es 1 día por llamado
## Comentarios finales
Tener en cuenta que el formato de fecha que recibe la API es YYYY-MM-DD

## Soluciones diseñadas (No requiere desarollar código)

Tal como se indicó al inicio, el equipo de Analítica ha diseñado dos aproximaciones para consumir el servicio en los siguientes lenguajes:

|Lenguaje|Nombre de Script o Archivo|
|--------|--------------------------|
|Python| pydataxm.py|
|Excel (VBA) | Macro.xlsm|

## Lista de métricas disponibles y datos requeridos para su uso
A continuación, presentamos el listado de métricas disponibles y los parámetros requeridos para realizar peticiones de información.
| Nombre de variable                                                             | Unidad de medida | Granularidad | Parámetros                                                                                                | URL                               |
|--------------------------------------------------------------------------------|------------------|--------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------|
| Consumo Combustible Recursos pertenecientes al Despacho Central                | MBTU             | Horaria      | {"MetricId": "ConsCombustibleMBTU","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Recurso"}  | http://servapibi.xm.com.co/hourly |
| Generación Real por recurso                                                    | kWh              | Horaria      | {"MetricId": "Gene","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Recurso"}                 | http://servapibi.xm.com.co/hourly |
| Generación Real (Total SIN)                                                    | kWh              | Horaria      | {"MetricId": "Gene","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}                 | http://servapibi.xm.com.co/hourly |
| Demanda Comercial por Agente                                                   | kWh              | Horaria      | {"MetricId": "DemaCome","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Agente"}              | http://servapibi.xm.com.co/hourly |
| Demanda Comercial (Total SIN)                                                  | kWh              | Horaria      | {"MetricId": "DemaCome","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}             | http://servapibi.xm.com.co/hourly |
| Precio de Oferta del Despacho                                                  | $COP/kWh         | Horaria      | {"MetricId": "PrecOferDesp","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Recurso"}         | http://servapibi.xm.com.co/hourly |
| Precio de Bolsa Nacional                                                       | $COP/kWh         | Horaria      | {"MetricId": "PrecBolsNaci","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}         | http://servapibi.xm.com.co/hourly |
| Máximo Precio de Oferta Nacional                                               | $COP/kWh         | Horaria      | {"MetricId": "MaxPrecOferNal","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}       | http://servapibi.xm.com.co/hourly |
| Precio de Escasez de Activación                                                | $COP/kWh         | Diaria       | {"MetricId": "PrecEscaAct","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}          | http://servapibi.xm.com.co/daily  |
| Restricciones Aliviadas (Total SIN)                                            | $COP             | Horaria      | {"MetricId": "RestAliv","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Sistema"}             | http://servapibi.xm.com.co/hourly |
| Listado de recursos térmicos con su respectiva Capacidad Efectiva Neta por mes | KW               | Mensual      | {"MetricId": "CapEfecNeta","StartDate": "2018-01-01","EndDate": "2018-12-31","Entity":"Sistema"}          | http://servapibi.xm.com.co/annual |
| Generación Ideal                                                               | kWh              | Horaria      | {"MetricId": "GeneIdea","StartDate": "2018-01-01","EndDate": "2018-01-01","Entity":"Sistema"}             | http://servapibi.xm.com.co/hourly |
| Volumen Útil en Energía                                                        | kWh              | Diaria       | {"MetricId": "VoluUtilDiarEner","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Sistema"}     | http://servapibi.xm.com.co/daily  |
| Aportes Energía                                                                | kWh              | Diaria       | {"MetricId": "AporEner","StartDate": "2019-01-01","EndDate": "2019-01-31","Entity":"Sistema"}             | http://servapibi.xm.com.co/daily  |
| Remuneración Real Individual Diaria del Cargo por Confiabilidad– RRID          | $COP             | Diaria       | {"MetricId": "RemuRealIndiv","StartDate": "2020-01-01","EndDate": "2020-01-31","Entity":"Sistema"}        | http://servapibi.xm.com.co/daily  |
| Generación Ideal por Recurso                                                   | kWh              | Horaria      | {"MetricId": "GeneIdea", "StartDate": "2015-01-01", "EndDate": "2015-01-31", "Entity" : "Recurso"}        | http://servapibi.xm.com.co/hourly |
| Precio Promedio Contratos Regulado                                             | $COP/kWh         | Diaria       | {"MetricId": "PrecPromContRegu", "StartDate": "2015-01-01",EndDate": "2015-01-31","Entity" : "Sistema"}   | http://servapibi.xm.com.co/daily  |
| Precio Promedio Contratos No Regulado                                          | $COP/kWh         | Diaria       | {"MetricId": "PrecPromContNoRegu", "StartDate": "2015-01-01",EndDate": "2015-01-31","Entity" : "Sistema"} | http://servapibi.xm.com.co/daily  |
| Ventas en Contratos Energía por Agente                                         | kWh              | Horaria      | {"MetricId": "VentContEner","StartDate": "2015-01-01","EndDate": "2015-01-31","Entity" : "Agente"}        | http://servapibi.xm.com.co/hourly |
| Ventas en Contratos Energía (Total SIN)                                        | kWh              | Horaria      | {"MetricId": "VentContEner","StartDate": "2015-01-01","EndDate": "2015-01-31","Entity" : "Sistema"}       | http://servapibi.xm.com.co/hourly |
| Compras en Contrato Energía por Agente                                         | kWh              | Horaria      | {"MetricId": "CompContEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}       | http://servapibi.xm.com.co/hourly |
| Compras en Contrato Energía (Total SIN)                                        | kWh              | Horaria      | {"MetricId": "CompContEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}      | http://servapibi.xm.com.co/hourly |
| Compras en Bolsa Nacional Energía por Agente                                   | kWh              | Horaria      | {"MetricId": "CompBolsNaciEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}   | http://servapibi.xm.com.co/hourly |
| Compras en Bolsa Nacional Energía (Total SIN)                                  | kWh              | Horaria      | {"MetricId": "CompBolsNaciEner","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}  | http://servapibi.xm.com.co/hourly |

 

