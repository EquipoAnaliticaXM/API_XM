from distutils.core import setup
setup(
  name = 'pydataxm',         # How you named your package folder (MyLib)
  packages = ['pydataxm'],   # Chose the same as "name"
  version = '0.3.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Choose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Interface to play with the API XM',   # Give a short description about your library
  author = 'Equipo Analitica XM',                   # Type in your name
  author_email = 'analitica@xm.com.co',      # Type in your E-Mail
  url = 'https://github.com/EquipoAnaliticaXM/API_XM',   # Provide either the link to your github or to your website
  download_url = 'https://raw.githubusercontent.com/EquipoAnaliticaXM/API_XM/master/pydataxm/pydataxm.py',    # I explain this later on
  keywords = ['API interpreter','Mercado Energía Mayorista', 'XM'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests', 'pandas','datetime'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6']
)