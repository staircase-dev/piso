# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# from numpydoc.docscrape import NumpyDocString
# from sphinx.ext.autosummary import _import_by_name


import inspect

# for sphinx
import os
import sys
from datetime import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import piso  # isort:skip

# for nbsphinx
os.environ["PYTHONPATH"] = os.path.abspath(parentdir)


# -- Project information -----------------------------------------------------

project = "piso"
copyright = f"2021-{datetime.now().year}, Riley Clement"
author = "Riley Clement"
version = piso.__version__
if "untagged" in version:
    version = "latest"
elif "unknown" in version:  # for when not installed
    try:
        import toml

        version = dict(toml.load(parentdir + "/pyproject.toml"))["tool"]["poetry"][
            "version"
        ]
    except:  # noqa E722
        pass
version = version.split("+")[0]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx.ext.extlinks",
    # "sphinx.ext.linkcode",
    "numpydoc",  # handle NumPy documentation formatted docstrings]
    "nbsphinx",
    "sphinx_design",
]

source_suffix = [".rst"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
]

suppress_warnings = [
    "nbsphinx.ipykernel",
]

autosummary_generate = True

# sphinx-panels shouldn't add bootstrap css since the pydata-sphinx-theme
# already loads it
# panels_add_bootstrap_css = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

master_doc = "index"


intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "staircase": ("https://www.staircase.dev/en/latest", None),
}


latex_elements = {
    "preamble": r"""
\usepackage{amssymb}
""",
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "github_url": "https://github.com/staircase-dev/piso",
    "navbar_end": ["navbar-icon-links"],
}

html_theme_options["analytics"] = {
    "google_analytics_id": "UA-65430466-3",
}

html_show_sourcelink = False


html_logo = "img/piso_white.svg"
html_favicon = "img/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

html_context = {
    # ...
    "default_mode": "light"
}


def setup(app):
    app.add_css_file("custom.css")
