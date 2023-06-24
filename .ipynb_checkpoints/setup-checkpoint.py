from setuptools import setup

setup(name='pypacity',
      version='0.1',
      description='Ampacity computation Package',
      # url='https://github.com/mmanana/pypacity',
      author='Universidad de Cantabria. DIEE. GTEA',
      author_email='mananam@unican.es',
      license='GNU',
      packages=['cable', 'case', 'ieee738', 'cigre601', 'pvsystems'],
      zip_safe=False)
