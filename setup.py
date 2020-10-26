from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='cpu_load_generator',
      version='0.1',
      description='CPU load generator',
      long_description=long_description,
      url='https://github.com/GaetanoCarlucci/CPULoadGenerator',
      author='Gaetano Carlucci',
      author_email='gaetano.carlucci@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['psutil', 'matplotlib']
      )
