from distutils.core import setup
setup(
  name = 'pydataxm',       
  packages = ['pydataxm'],  
  version = '0.3.13',     
  license='MIT', 
  description = 'Interface to play with the API XM and API SIMEM',
  author = 'Equipo Analitica XM',
  requires_python = '>=3.10',
  author_email = 'analitica@xm.com.co',
  url = 'https://github.com/EquipoAnaliticaXM/API_XM',
  download_url = 'https://raw.githubusercontent.com/EquipoAnaliticaXM/API_XM/master/pydataxm/pydataxm.py',   
  keywords = ['API interpreter','Mercado Energía Mayorista', 'XM', 'SIMEM'],   
  install_requires=['requests', 'pandas','datetime', 'aiohttp', 'asyncio', 'nest_asyncio', 'plotly'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3.10']
)