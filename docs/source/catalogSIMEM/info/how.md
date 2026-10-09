# Inicialización de un objeto de la clase

Para poder acceder a las funcionalidades de la clase primero se debe inicializar un objeto de la clase.

## Uso

Para inicializar un objeto de la clase hay 2 formas:

1. Inicializar catálogo de variables:

```bash
from pydataxm.pydatasimem import CatalogSIMEM

catalog_variables = CatalogSIMEM(catalog_type='Variables')
```

2. Inicializar catálogo de conjuntos de datos:

```bash
from pydataxm.pydatasimem import CatalogSIMEM

catalog_datasets = CatalogSIMEM(catalog_type='Datasets')
```