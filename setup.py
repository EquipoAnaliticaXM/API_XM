from setuptools import setup, find_packages

setup(
    name='pydataxm',
    version='0.3.15',
    packages=find_packages(),
    license='MIT',
    description='Interface to interact with API XM and API SIMEM',
    author='Equipo Analitica XM',
    author_email='analitica@xm.com.co',
    url='https://github.com/EquipoAnaliticaXM/API_XM',
    download_url='https://raw.githubusercontent.com/EquipoAnaliticaXM/API_XM/master/pydataxm/pydataxm.py',
    python_requires='>=3.10',
    install_requires=[
        'pandas>=2.2.3',
        'numpy',
        'requests',
        'aiohttp',
        'asyncio',
        'nest_asyncio'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
