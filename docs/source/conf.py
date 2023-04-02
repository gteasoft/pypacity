# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys 

sys.path.insert( 0, os.path.abspath('../..')) 



project = 'pypacity'
copyright = '2022, Mario Mañana Canteli'
author = 'Mario Mañana Canteli'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser',
            'sphinx.ext.autodoc', # Core library for html generation from docstrings
            'sphinx.ext.autosummary',   # Create neat summary tables
            'sphinx.ext.napoleon',      # Support for NumPy and Google style docstring
              ]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

#import os
#import sys
#sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'cable')))
#sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'ieee738')))

sys.path.insert(0, os.path.abspath(os.path.join('../../cable')))
sys.path.insert(0, os.path.abspath(os.path.join('../../ieee738')))
sys.path.insert(0, os.path.abspath(os.path.join('../../case')))

