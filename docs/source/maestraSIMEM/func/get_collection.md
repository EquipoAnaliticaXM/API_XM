# Obtener colección de maestras

Esta función le permite al usuario obtener el listado de maestras disponibles que se pueden usar dentro de la clase MaestraSIMEM.

## Uso

Para obtener los datos se debe ejecutar la siguiente instrucción:

```bash

from pydataxm.pydatasimem import MaestraSIMEM

listado_maestras = MaestraSIMEM.get_collection()
print(listado_maestras)

```

## Información

La información que se puede encontrar dentro de esta función es la siguiente:

- **Maestra:** Código de la maestra dentro de MaestraSIMEM.
- **Descripción:** Descripción detallada de la maestra.
- **Cruces:** Contiene una lista de claves que definen los cruces de una maestra, esta columna indica con qué otras maestras se puede hacer join simulando un modelo tipo OLAP. Es clave para entender la granularidad y las relaciones entre datos.

## Ejemplo

El dataframe que se le devuelve al usuario viene de la siguiente forma:

| Maestra | Descripción                                                                | Cruces                                           |
|---------|----------------------------------------------------------------------------| ------------------------------------------------ |  
| Agente  | Listado de agentes registrados en el mercado por actividad y para cada dia | []                                               |
| Planta  | Listado de las plantas de generacion registradas                           | ['CodigoSICAgente', 'CodigoSubAreaOperativa', 'CodigoAreaOperativa'] |
| ....... | .......................................................................... | .......................................................................... |
