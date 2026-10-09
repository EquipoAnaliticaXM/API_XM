# Obtener colección de variables

Esta función le permite al usuario obtener el listado de variables disponibles que se pueden usar dentro de la clase VariableSIMEM.

## Uso

Para obtener los datos se debe ejecutar la siguiente instrucción:

```bash

from pydataxm.pydatasimem import VariableSIMEM

listado_variables = VariableSIMEM.get_collection()
print(listado_variables)

```

## Información

La información que se puede encontrar dentro de esta función es la siguiente:

- **CodigoVariable:** Código de la variable dentro de SIMEM.
- **Nombre:** Nombre completo de la variable.
- **Dimensiones:** Contiene una lista de claves que definen las dimensiones de una variable, esta columna indica con qué otras variables se puede hacer join simulando un modelo tipo OLAP. Es clave para entender la granularidad y las relaciones entre datos.

## Ejemplo

El dataframe que se le devuelve al usuario viene de la siguiente forma:

| CodigoVariable | Nombre                   | Dimensiones         |
|----------------|--------------------------| ------------------- |  
| PB_Nal         | Precio de bolsa nacional | [FechaHora,Version] |
| PrecioEscasez  | Precio de escasez        | [Fecha]             |
| .............. | ........................ | ................... |
