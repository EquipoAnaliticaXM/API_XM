# Descripción estadística de la variable

Esta función le permite al usuario obtener la descripción estadística de la variable solicitada.

## Valores estadísticos

- Media: Es el promedio de todos los valores. Se calcula sumando todos los valores y dividiéndolos por el número total de valores.
- Mediana: Es el valor que se encuentra en el medio de un conjunto de datos ordenados. Si el número de valores es par, es el promedio de los dos valores centrales.
- Desviació estándar: Mide la cantidad de variación o dispersión de un conjunto de valores. Una desviación estándar baja indica que los valores tienden a estar cerca de la media, mientras que una alta indica que los valores están más dispersos.
- Mínimo: Es el valor más pequeño en el conjunto de datos.
- Máximo: Es el valor más grande en el conjunto de datos.
- Cantidad de nulos: Indica cuántos valores en el conjunto de datos son nulos o faltantes.
- Cantidad de ceros: Indica cuántos valores en el conjunto de datos son exactamente cero.
- Fecha inicial: Indica el primer día del rango de fechas para el cual se han recopilado los datos.
- Fecha final: Indica el último día del rango de fechas para el cual se han recopilado los datos.
- Granularidad: Indica el nivel de detalle temporal de los datos. Puede ser diaria, semanal, mensual, etc.

## Uso

Para obtener la descripción estadística se debe ejecutar la siguiente instrucción:

```bash

from pydataxm.pydatasimem import VariableSIMEM

CodigoVariable = "PrecioEscasez"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"

var = VariableSIMEM(CodigoVariable, Fecha_Inicio, Fecha_Fin)
var.describe_data()

```

## Ejemplo

El resultado viene en diccionario de la siguiente forma:

```bash
stats = {
            'mean': 50.20,
            'median': 55.34,
            'std_dev': 2.27,
            'min': 84.45,
            'max': 30.75,
            'null_count': 0,
            'zero_count': 0,
            'start_date': 2024-01-01,
            'end_date': 2024-01-31,
            'granularity': diaria
        }
        
```
