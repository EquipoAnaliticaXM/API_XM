Documentación pydatasimem
=========================================================

Este repositorio se crea con el fin de compartir una herramienta de consulta open source para extraer información relevante del Mercado de Energía Mayorista colombiano usando la api SIMEM. Dentro de la librería se podrán encontrar 4 clases cada una con una funcionalidad y un objetivo en específico; son las siguientes:

Clase CatalogSIMEM
========================
En este apartado se encuentra toda la información relacionada a la clase CatalogSIMEM y sus diferentes funcionalidades. Esta clase está enfocada a la lectura y exploración del catálogo tanto de variables como de conjuntos de datos que hay en SIMEM.

.. toctree::
   :maxdepth: 1
   :caption: Documentación clase CatalogSIMEM:

   catalogSIMEM/index.rst

Clase ReadSIMEM
========================
En este apartado se encuentra toda la información relacionada a la clase ReadSIMEM y sus diferentes funcionalidades. Esta clase está enfocada a la obtención, filtrado y exploración de los conjuntos de datos de SIMEM.

.. toctree::
   :maxdepth: 1
   :caption: Documentación clase ReadSIMEM:

   readSIMEM/index.rst

Clase VariableSIMEM
========================
En este apartado se encuentra toda la información relacionada a la clase VariableSIMEM y sus diferentes funcionalidades. Al igual que la clase ReadSIMEM, VariableSIMEM también está enfocada en la obtener y explorar datos pero en lugar de buscar a través de los conjuntos de datos, se busca a través de las variables.

.. toctree::
   :maxdepth: 1
   :caption: Documentación clase VariableSIMEM:

   variableSIMEM/index.rst

Clase MaestraSIMEM
========================
En este apartado se encuentra toda la información relacionada a la clase MaestraSIMEM y sus diferentes funcionalidades. Esta clase sigue la misma lógica de VariableSIMEM, pero en lugar de estar enfocada en la consulta de variables, se enfoca en la consulta de los datos maestros de SIMEM.

.. toctree::
   :maxdepth: 1
   :caption: Documentación clase MaestraSIMEM:

   maestraSIMEM/index.rst

Generación del json de listado de variables
==============================================
En este apartado se encuentra toda la información relacionada a la implementación del mapeo de variables a través de un json de configuración.

.. toctree::
   :maxdepth: 1
   :caption: Documentación json listado de variables:

   json/index.rst