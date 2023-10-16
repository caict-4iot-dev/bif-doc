# Configuration file for the Sphinx documentation builder.

# -- Project information

project = '星火链开发指南2.0'
copyright = '2023, 中国信息通信研究院'
author = '中国信息通信研究院'

release = '2.0.0'
version = '2.0.0'

# -- General configuration

extensions = [
    'myst_parser',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
html_static_path = ['_static']
# -- Options for HTML output

#html_theme = 'sphinx_rtd_theme'

html_logo = './_static/favicon.ico'

# -- Options for EPUB output
epub_show_urls = 'footnote'
