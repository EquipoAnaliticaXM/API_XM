# Obtener datos de un conjunto

Esta función le permite al usuario obtener los datos de un conjunto como un dataframe de la librería pandas.

## Uso

Para obtener los datos de algún conjunto se debe ejecutar una de las siguientes instrucción:

1. Con un conjunto de datos sin filtro:

```bash

from pydataxm.pydatasimem import ReadSIMEM

Dataset_id = "EC6945"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"

simem = ReadSIMEM(Dataset_id, Fecha_Inicio, Fecha_Fin)
data = simem.main()
```

2. Con un conjunto de datos con filtros:

```bash

from pydataxm.pydatasimem import ReadSIMEM

Dataset_id = "EC6945"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"
Filtro = ["CodigoVariable","=","PB_Nal"]

simem = ReadSIMEM(Dataset_id, Fecha_Inicio, Fecha_Fin, Filtro)
data = simem.main(filter=True)
```

Es importante conocer como se crean los filtros para poder usarlos correctamente, estos son manejados mediante el uso de listas bajo el formato ["Columna","Operación","Valor"]. Para el caso de uso de múltiples filtros se usa la misma estructura en una lista de listas de la siguiente forma:

[["Columna_1","Operación_1","Valor_1"],["Columna_2","Operación_2","Valor_2"],["Columna_2","Operación_3","Valor_3"]]

Las operaciones permitidas dentro de los filtros son : "=", "!=", "like", "!like", "in", "!in", ">", ">=", "<", "<=", "between", "!between"

Dentro de estas operaciones solamente "in", "!in", "between", "!between" no usan un único valor, para estas 4 operaciones los valores se deben pasar en una lista como en el siguiente ejemplo:

["Columna_1","between",["Valor_1","Valor_2"]]                     -- Operaciones between reciben únicamente 2 valores
["Columna_1","in",["Valor_1","Valor_2","Valor_3","Valor_4"...]]   -- Operaciones in reciben desde 1 valor