
# Configuration file for the Sphinx documentation builder.

# -- Project information 
project = 'FITMIND: Exercise & Stress Tracker'
copyright = '2025, Group 3D SETAP'
author = 'Group 3D'

release = '1.0'
version = '1.0.0'

# -- General configuration 
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
exclude_patterns = []

# Important: tells Sphinx which file to use as the root
master_doc = 'index'

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
