# Obtener datos

Esta función le permite al usuario obtener los datos como un dataframe de la librería pandas. Este dataframe puede venir indexado de 2 formas según las columnas del conjunto de datos.

## Tipos de dataframe según el índice

1. Indexado por cruces y por fecha: Este dataframe contiene las columnas originales que vienen desde el portal SIMEM, pero la columna fecha y las columnas que pertenecen a los cruces vienen como índices.
2. Indexado por fecha: Cuando el dataframe no viene con cruces solamente se indexa por la columna fecha.

## Uso

Para obtener los datos se debe ejecutar la siguiente instrucción:

```bash

from pydataxm.pydatasimem import MaestraSIMEM

Maestra = "Agente"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"

mta = MaestraSIMEM(Maestra, Fecha_Inicio, Fecha_Fin)
mta.get_data()

```

## Filtros

El uso de filtros es opcional, pero si se desean utilizar es importante saber cómo hacerlo, estos son manejados mediante el uso de listas bajo el formato ["Columna","Operación","Valor"]. Para el caso de uso de múltiples filtros se usa la misma estructura en una lista de listas de la siguiente forma:

[["Columna_1","Operación_1","Valor_1"],["Columna_2","Operación_2","Valor_2"],["Columna_2","Operación_3","Valor_3"]]

Las operaciones permitidas dentro de los filtros son : "=", "!=", "like", "!like", "in", "!in", ">", ">=", "<", "<=", "between", "!between"

Dentro de estas operaciones solamente "in", "!in", "between", "!between" no usan un único valor, para estas 4 operaciones los valores se deben pasar en una lista como en el siguiente ejemplo:

["Columna_1","between",["Valor_1","Valor_2"]]                     -- Operaciones between reciben únicamente 2 valores
["Columna_1","in",["Valor_1","Valor_2","Valor_3","Valor_4"...]]   -- Operaciones in reciben desde 1 valor

## Ejemplo

```bash

from pydataxm.pydatasimem import MaestraSIMEM

Maestra = "Agente"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"
Filtro = ["ActividadAgente","in",["Distribuidor","Transportador"]]

mta = MaestraSIMEM(Maestra, Fecha_Inicio, Fecha_Fin, Filtro)
mta.get_data()

```