# Inicialización de un objeto de la clase

Para poder acceder a las funcionalidades de la clase primero debemos inicializar un objeto de la clase, para lo cual se necesitan varios parámetros que se explicaran más adelante.

## Parámetros

- CodigoVariable: Código de la variable que se desea explorar.
- Fecha_Inicio: Fecha desde la cual se necesita la información.
- Fecha_Fin: Fecha hasta la que se necesita la información.
- Version (Opcional): Versión que se requiere de la variable. Este parámetro recibe dos tipos de valores: una versión específica como texto como bien puede ser `TXF` o `TX5`, o un número refiriendose al orden de las versiones (0 para última, -1 para la penúltima, -2 para la antepenúltima, - 3 para la trasantepenúltima, y así sucesivamente......). En caso de que no ingrese un valor siempre se tomara la última versión.
- Filtro (Opcional): Lista de filtros a aplicar a la información.
- quality_check (Opcional): Valor que solo puede ser verdadero o falso. Este parámetro solamente afecta la función de obtener datos en la forma en la que se devuelve el dataframe, para más información diríjase al apartado de `Funcionalidades` y `Obtener datos`.

## Uso

Para inicializar un objeto de la clase hay 2 formas:

1. Parámetro `Version` como texto:

```bash

from pydataxm.pydatasimem import VariableSIMEM

CodigoVariable = "PrecioEscasez"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"
Version = "TXF"
Filtro = ["Valor",">","100"]
quality_check = False

var = VariableSIMEM(CodigoVariable, Fecha_Inicio, Fecha_Fin, Version, Filtro, quality_check)
```

2. Parámetro `Version` como número:

```bash

from pydataxm.pydatasimem import VariableSIMEM

CodigoVariable = "PrecioEscasez"
Fecha_Inicio = "2024-01-01"
Fecha_Fin = "2024-12-31"
Version = 0
Filtro = ["Valor",">","100"]
quality_check = False

var = VariableSIMEM(CodigoVariable, Fecha_Inicio, Fecha_Fin, Version, Filtro, quality_check)
```