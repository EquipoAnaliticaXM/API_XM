# Inicialización de un objeto de la clase

Para poder acceder a las funcionalidades de la clase primero debemos inicializar un objeto de la clase, para lo cual se necesitan varios parámetros que se explicaran más adelante.

## Parámetros

- Maestra: Código de la maestra que se desea explorar.
- Fecha_Inicio: Fecha desde la cual se necesita la información.
- Fecha_Fin: Fecha hasta la que se necesita la información.
- Filtro (Opcional): Lista de filtros a aplicar a la información.

## Uso

Para inicializar un objeto de la clase se hace de la siguiente manera:

```bash

from pydataxm.pydatasimem import MaestraSIMEM

Maestra = "Agente"
Fecha_Inicio = "2026-01-01"
Fecha_Fin = "2026-01-31"
Filtro = ["ActividadAgente","=","Distribuidor"]

var = VariableSIMEM(Maestra, Fecha_Inicio, Fecha_Fin, Filtro)
```