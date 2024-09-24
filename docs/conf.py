"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# Disable message for naming convention in this file,
# because we must comply to the sphinx naming convention
# pylint: disable-msg=invalid-name

import os
import sys


source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))

sys.path.insert(0, source_path)
print(sys.path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'lily-unit-test'
project_copyright = '2024, LilyTronics'
author = 'LilyTronics'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc'
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
