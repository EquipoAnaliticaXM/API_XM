# API XM
Este repositorio se crea con el fin de compartir herramientas de consulta para extraer información relevante del Mercado de Energía Mayorista colombiano

## Variables disponibles

A continuacion se listan las variables que se encuentran disponibles para su consulta:

* Generación Real del SIN y por Recurso de Generación
* Generación por tipo de Despacho / Tipo de Fuente
* Demanda Comercial del SIN y por Agente Comercializador
* Costo de las Restricciones que se trasladan a la demanda (Restricciones finales)
* Precio de Bolsa Nacional
* Máximo Precio de Oferta
* Precio de Escasez de Activación
* Generación Ideal
* Generación Ideal por Recurso
* Volumen Útil Diario (Energía)
* Aportes Diarios (Energía)
* Remuneración Real Individual Diaria del Cargo por Confiablidad (RRID)
* Consumo de Combustible
* Precio de Oferta del Despacho
*  Precio Promedio Contratos Regulado
* Precio Promedio Contratos No Regulado
* Ventas en Contratos Energía por Agente
* Ventas en Contratos Energía (Total SIN)
* Compras en Contrato Energía por Agente
* Compras en Contrato Energía (Total SIN)
* Compras en Bolsa Nacional Energía por Agente
* Compras en Bolsa Nacional Energía (Total SIN)



Para consumir el servicio se presenta una aproximación propuesta por el equipo de Analítica de XM en los siguientes lenguajes:

|Lenguaje|Nombre de Script o Archivo|
|--------|--------------------------|
|Python| RequestDataAPI.py|
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
| Generación por tipo de despacho y tipo de fuente                               | kWh              | Horaria      | {"MetricId": "Gene","StartDate": "2018-01-01","EndDate": "2018-01-02","Entity":"Renovabilidad"}           | http://servapibi.xm.com.co/hourly |
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
## Comentarios Finales
Tener en cuenta que el formato de fecha que recibe la API es YYYY-MM-DD
 
## Restricciones de consulta:
Con el fin de evitar saturar el servicio, se han establecido restricciones a las consultas así:
* Para datos horarios y diarios, máximo 30 días por llamado
* Para datos anuales, máximo 366 días por llamado

