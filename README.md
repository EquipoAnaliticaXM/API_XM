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
* Demanda Comercial Regulada por Agente
* Demanda Comercial No regulada por Agente
* Demanda Comercial Regulada (Total SIN)
* Demanda Comercial No Regulada (Total SIN)
* Demanda Comercial No Regulada por CIIU

### Oferta y Generación
* Generación Real Total 
* Generación Real por Recurso (Planta de Generación)
* Generación Ideal
* Generación Ideal por Recurso (Planta de Generación)
* Consumo de Combustible por Recurso (Planta de Generación)
* Listado de Recursos de generación con sus principales atributos (Agente Generador, Tipo, Capacidad Efectiva Neta, entre otros)
* Generación de Seguridad por Recurso
* Generación Fuera de Mérito por Recurso
* Obligaciones de Energía Firme por Recurso
* Generación Programada Despacho
* Generación Programada Redespacho
* Disponibilidad Real
* Disponibilidad Comercial
* Disponibilidad Declarada
* Reconciliación Positiva Energía
* Reconciliación Negativa Energía
* Desviaciones Energía
* Compras AGPE

### Transacciones y Precios
* Costo de las Restricciones que se trasladan a la demanda (Restricciones finales)
* Precio de Escasez de Activación
* Precio de Bolsa Nacional
* Máximo Precio de Oferta
* Remuneración Real Individual Diaria del Cargo por Confiablidad (RRID)
* Precio de Oferta del Despacho
* Precio Promedio Contratos Regulado
* Precio Promedio Contratos No Regulado
* Ventas en Contratos Energía por Agente
* Ventas en Contratos Energía (Total SIN)
* Compras en Contrato Energía por Agente
* Compras en Contrato Energía (Total SIN)
* Compras en Bolsa Nacional Energía por Agente
* Compras en Bolsa Nacional Energía (Total SIN)
* Responsabilidad Comercial AGC
* Reconciliación Positiva Moneda
* Reconciliación Negativa Moneda
* Restricciones sin alivios
* Restricciones aliviadas
* Desviaciones Moneda
* DDV Contratada
* FAZNI Moneda
* FAER Moneda
* PRONE Moneda
* MC
#### Intercambios Internacionales
* Importaciones en Energía
* Exportaciones en Energia
### Cálculo de emisiones de CO2
* Emisiones de CO2
* Emisiones de CH4
* Emisiones de N2O
* Emisiones de CO2eq
* Consumo Combustible Aproximado para el Factor Emisión
* Factor de Emisión de la Matriz Energética (CO2eq/kWh)

### Listados
* Listado Recursos con atributos
* Listado de agentes con atributos
* Listado de métricas

## Filtros (Parámetro Opcional)

Con este parámetro se permite extraer datos para una serie de entidades personalizada. Las métricas que pueden ser filtradas son todas aquellas que tienen cruces por:

1. Agente (código bdMEM del agente _i.e._ CASC, EPMC, ENDG, entre otros)
2. Recurso (código bdMEM del recurso _i.e._ EPFV, TBST, JEP1, entre otros)
3. Embalse
4. Río

Para conocer el detalle de los bdMEM de cada recurso o agente le invitamos a consultar las métricas _ListadoRecursos_ y _ListadoAgentes_ disponibles en este mismo servicio.

## Restricciones de la API:
Con el fin de evitar saturar el servicio, se han establecido restricciones a las consultas así:
* Para datos horarios y diarios, máximo 30 días por llamado
* Para datos mensuales, máximo 731 días por llamado
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
| Precio Promedio Contratos Regulado                                    | $COP/kWh         | Diaria       | {"MetricId": "PrecPromContRegu", "StartDate": "2015-01-01",EndDate": "2015-01-31","Entity" : "Sistema"}   | http://servapibi.xm.com.co/daily   |
| Precio Promedio Contratos No Regulado                                 | $COP/kWh         | Diaria       | {"MetricId": "PrecPromContNoRegu", "StartDate": "2015-01-01",EndDate": "2015-01-31","Entity" : "Sistema"} | http://servapibi.xm.com.co/daily   |
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
| Demanda Comercial Regulada (Total SIN)                                | kWh              | Horaria      | {"MetricId": "DemaComeReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Agente"}        | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial No Regulada (Total SIN)                             | kWh              | Horaria      | {"MetricId": "DemaComeNoReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}     | http://servapibi.xm.com.co/hourly  |
| Restricciones sin alivios                                             | $COP             | Horaria      | {"MetricId": "RestSinAliv","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "Sistema"}       | http://servapibi.xm.com.co/hourly  |
| Demanda Comercial No Regulada por CIIU                                | kWh              | Horaria      | {"MetricId": "DemaComeNoReg","StartDate": "2015-01-01", "EndDate": "2015-01-31","Entity" : "CIIU"}        | http://servapibi.xm.com.co/hourly  |
| Listado Recursos con atributos                                        | NA               | Lista        | {"MetricId": "ListadoRecursos","Entity" : "Sistema"}                                                      | http://servapibi.xm.com.co/lists   |
| Listado de agentes con atributos                                      | NA               | Lista        | {"MetricId": "ListadoAgentes" ,"Entity" : "Sistema"}                                                      | http://servapibi.xm.com.co/lists   |
