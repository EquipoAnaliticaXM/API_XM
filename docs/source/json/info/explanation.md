# Información general json

La existencia de un json de configuración surgió debido a la necesidad de consultar la información del SIMEM modelando a través de variables y maestras, por lo que fue necesario contar con un insumo que permitiera conocer las características/parámetros de cada una de las variables y de las maestras que se desearan consultar. El json usa  está dividido en 2 secciones: variables y maestras; ambas siguiendo la misma estructura.

## Parámetros

- **name:** Nombre completo de la variable/maestra
- **dataset_id:** Id del dataset donde se encuentra la variable/maestra, si se encuentra en más de uno se selecciona el de mínima granularidad.
- **var_column:** Nombre de la columna en la que se encuentra el código de la variable dentro del dataset, esto solo aplica cuándo la variable se encuentra en registros, en otro caso se coloca `null`.
- **value_column:** Nombre de la columna en la que se encuentra el valor de la variable dentro del dataset.
- **version_column:** Nombre de la columna en la que se encuentra la versión de la variable dentro del dataset, en caso de no tener se coloca `null`.
- **date_column:** Nombre de la columna en la que se encuentra la fecha dentro del dataset.
- **dimensions:** Además de la fecha y/o la versión es posible que la variable/maestra posea más dimensiones, es en este parámetro donde se agregan dentro de una lista donde en caso de no tener más dimensiones se coloca `[]` y en caso de tener se sigue la forma `["dimension_1", "dimension_2", ...]`.
- **maestra_column:** Nombre del dato maestro relacionado a la variable dnetro del catálogo de variables.
- **codMaestra_column:** Nombre del código maestra relacionado en el dataset.
- **esTx2PrimeraVersion:** Este parámetro solo puede tener dos valores, `0` si la primera versión de la variable es TX1 o `1` si la primera versión de la variables es TX2

## Ejemplo

Una variable dentro del json se vería de la siguiente forma:

```bash

"GIdeal": {
      "name": "Generación ideal total",
      "dataset_id": "2d5afe",
      "var_column": "CodigoVariable",
      "value_column": "ValorTexto",
      "version_column": "Version",
      "date_column": "FechaHora",
      "dimensions": ["CodigoPlanta"],
      "maestra_column": "Planta",
      "codMaestra_column": "CodigoPlanta",
      "esTX2PrimeraVersion": 0
    }
```
