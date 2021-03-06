from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='cpu-load-generator',
      version='0.1',
      description='CPU load generator',
      long_description=long_description,
      url='https://github.com/sirtyman/CPULoadGenerator',
      author='Marcin Tyman',
      author_email='marcin.tyman@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['psutil']
      )
