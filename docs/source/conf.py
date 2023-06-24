# -*- coding: utf-8 -*-

import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pypacity'
copyright = '2023, Universidad de Cantabria. DIEE. GTEA'
author = 'Mario Mañana'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


#sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))
#sys.path.insert(0, os.path.abspath("../../.."))
#sys.path.insert(0, os.path.abspath("../../cable"))



#sys.path.append(os.path.abspath(".\\_themes"))
#sys.path.append(os.path.abspath("..\\tests"))
#sys.path.append(os.path.abspath("..\\network_generator"))
# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
#extensions = ['sphinx.ext.intersphinx', 'sphinx.ext.mathjax', 'sphinx.ext.autodoc', 
#              'sphinx.ext.autosummary'] #sphinx.ext.mathjax and sphinx.ext.imgmath don't comply with each other anymore., pngmath will be replaced by imgmath in new sphinx version
extensions = [ 'sphinx.ext.napoleon', 'sphinx_rtd_size', ]

sphinx_rtd_size_width = "90%"
napoleon_google_docstring = False





def setup(app):
    app.add_css_file('custom.css')


#extensions = [
#    'sphinx.ext.duration',
#]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_static_path = ['_static']
html_css_files = ['custom.css',]


#numfig = True
#language = 'ja'

#extensions.append('sphinx.ext.todo')
#extensions.append('sphinx.ext.autodoc')
#extensions.append('sphinx.ext.autosummary')
#extensions.append('sphinx.ext.intersphinx')
#extensions.append('sphinx.ext.mathjax')
#extensions.append('sphinx.ext.viewcode')
#extensions.append('sphinx.ext.graphviz')


autosummary_generate = True
#html_theme = 'default'
#source_suffix = ['.rst', '.txt']

autodoc_typehints = "description"

# Define the html theme
# https://www.sphinx-doc.org/en/master/usage/theming.html
html_theme = 'sphinx_rtd_theme' #'nature' #'sphinx_rtd_theme' # 'alabaster' #'bizstyle' # 'alabaster'


    
#sphinx_rtd_size_width = "90%"