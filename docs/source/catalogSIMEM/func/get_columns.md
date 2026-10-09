# Descripción estadística de la variable

Esta función le permite al usuario obtener las columnas que hay dentro de los catálogos.

## Uso

Para obtener las columnas de algún catálogo se debe ejecutar la siguiente instrucción:

```bash
from pydataxm.pydatasimem import CatalogSIMEM

catalog_variables = CatalogSIMEM(catalog_type='Variables')

catalog_variables.get_columns()
```

```bash
from pydataxm.pydatasimem import CatalogSIMEM

catalog_datasets = CatalogSIMEM(catalog_type='Datasets')

catalog_datasets.get_columns()
```

## Ejemplo

El resultado será de la siguiente forma:

| nameColumn | dataType | description |
|------------|----------|-------------|
| .......... | ........ | ..........  |