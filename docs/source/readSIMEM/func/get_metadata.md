# Obtener los metadatos de un conjunto

Esta función le permite al usuario obtener laos metadatos que hay dentro de un conjunto.

## Uso

Para obtener los metadatos de algún conjunto se debe ejecutar la siguiente instrucción:

```bash

from pydataxm.pydatasimem import ReadSIMEM

Dataset_id = "EC6945"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"

simem = ReadSIMEM(Dataset_id, Fecha_Inicio, Fecha_Fin)
simem.get_metadata()
```
