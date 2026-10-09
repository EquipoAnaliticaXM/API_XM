# Obtener datos del catálogo

Esta función le permite al usuario obtener los datos del catálogo como un dataframe de la librería pandas.

## Uso

Para obtener los datos de algún catálogo se debe ejecutar la siguiente instrucción:

```bash
from pydataxm.pydatasimem import CatalogSIMEM

catalog_variables = CatalogSIMEM(catalog_type='Variables')

df_catalog_variables = catalog_variables.get_data()
```

```bash
from pydataxm.pydatasimem import CatalogSIMEM

catalog_datasets = CatalogSIMEM(catalog_type='Datasets')

df_catalog_datasets = catalog_datasets.get_data()
```

## Ejemplo

El dataframe vendrá con distintas columnas dependiendo si es el catálogo de variables o el de conjuntos de datos, y serán de las siguientes formas:

1. Catálogo de variables:

| idDataset | nombreDataset | codigoVariable | nombreVariable | descripcion | unidadMedida | fechaPublicacion | fechaInicio | fechaFin |
|-----------|---------------|----------------|----------------|-------------|--------------|------------------|-------------|----------|
| ......... | ............. | .............  | .............. | ........... | ............ | ................ | ........... | ........ |

2. Catálogo de conjuntos de datos

| idDataset | nombreConjuntoDatos | fechaPublicacion | fechaActualizacion | inicioDato | finDato | fechaDescarga | urlConexionAPI | urlConjuntoDatos | tipoPublicacion |
|-----------|---------------------|------------------|--------------------|------------|---------|---------------|----------------|------------------|-----------------|
| ......... | ................... | ...............  | .................. | .......... | ....... | ............. | .............. | ................ | ............... |