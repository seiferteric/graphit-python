
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
      name = "graphit",
      version = "0.0.1",
      packages = find_packages(),
      install_requires=['distribute', 'requests>=1.1.0', 'yaml'],
      author = "Eric Seifert",
      author_email = "seiferteric@gmail.com",
      description = "Graphit.io Graphing API library",
      keywords = "graphit graph Graphit.io", 
      url = "http://www.graphit.io/",
      zip_safe = True,
      entry_points = {
        'console_scripts': [
          'graphit = graphit.cli:main'
        ]
      }
)
