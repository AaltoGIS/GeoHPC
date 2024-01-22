# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# from sphinx.util import SkipProgressMessage, progress_message

project = 'Spatial Data Analysis with High Performance Computing (HPC)'
copyright = 'GIST-Lab (2023), Aalto University'
author = 'Bryan R. Vallejo. GIST-Lab - Aalto University'
release = 'v1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx_togglebutton',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'myst_nb',
    'jupyter_sphinx',
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_book_theme'

# Show todos
todo_include_todos = True

# Add any paths that contain custom static files (such as style sheets)
html_static_path = ['_static']
html_logo = '_static/aalto-logo-web.png'
html_title = ""

html_theme_options = {
    # "external_links": [],
    "repository_url": "https://github.com/AaltoGIS/GeoHPC/",
    "repository_branch": "master",
    "path_to_docs": "source/",
    # "twitter_url": "https://twitter.com/pythongis",
    # "google_analytics_id": "UA-186242850-1",
    "use_edit_page_button": False,
    "use_repository_button": True,
    # "launch_buttons": {
    #     # "binderhub_url": "https://mybinder.org",
    #     "thebe": False,
    #     "notebook_interface": "jupyterlab",
    #     "collapse_navigation": False,
        # Google Colab does not provide an easy way for specifying/building/activating the conda environment
        # in a similar manner as Binder. Hence, let's not keep it. The easiest way seems to be:
        # https://github.com/jaimergp/condacolab
        # But it requires actions from the user nontheless, so atm it's a no-go.
        #"colab_url": "https://colab.research.google.com"
    # },
}

# Allow errors
nb_execution_allow_errors = True

# Do not execute cells
nb_execution_mode = "off"

suppress_warnings = ["myst.header"]