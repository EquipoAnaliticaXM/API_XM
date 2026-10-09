# Obtener información de interés de un conjunto

Además de los metadatos también es posible obtener información adicional de un conjunto que puede ser de utilidad e interés para el usuario.

## Funciones

Primero se inicailiza un objeto del conjunto de datos del que se desea conocer más información.

```bash

from pydataxm.pydatasimem import ReadSIMEM

Dataset_id = "EC6945"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"

simem = ReadSIMEM(Dataset_id, Fecha_Inicio, Fecha_Fin)
```

Estas son las distintas funciones que hay disponibles:

1. Obtener el nombre del conjunto de datos

```bash
simem.get_name()
```

2. Obtener las columnas del conjunto de datos

```bash
simem.get_columns()
```

3. Obtener el id del cojunto de datos

```bash
simem.get_datasetid()
```

4. Obtener la fecha inicial

```bash
simem.get_startdate()
```

5. Obtener la fecha final

```bash
simem.get_enddate()
```

6. Obtener la granularidad del conjunto de datos

```bash
simem.get_granularity()
```

7. Obtener la resolución del conjunto de datos

```bash
simem.get_resolution()
```

8. Obtener el filtro del conjunto de datos

```bash
simem.get_filters()
```