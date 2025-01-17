# -*- coding: utf-8 -*-
"""Sphinx documentation """


# -- Path setup --------------------------------------------------------------

from os.path import abspath, dirname
import sys

SETUP_PATH = abspath(dirname(dirname(__file__)))
sys.path.insert(0, SETUP_PATH)


# -- Get information from setup.py -------------------------------------------

# Get Package info
from setup import PACKAGE_INFO
SPHINX_INFO = PACKAGE_INFO['command_options']['build_sphinx']


# -- Project information -----------------------------------------------------

project = SPHINX_INFO['project'][1]
copyright = SPHINX_INFO['copyright'][1]
author = PACKAGE_INFO['author']
version = SPHINX_INFO['version'][1]
release = SPHINX_INFO['release'][1]


# -- Dynamically generates documentation from CLI help ----------

from subprocess import check_output


def _generates_rst(rst_path, content):
    """
    Generates a reStructuredText file with specified content.

    Args:
        rst_path (str): Path to ".rst" file
        content (list of str): File content lines.
    """
    with open(rst_path, 'wt', encoding='utf-8') as rst_file:
        rst_file.write('\n'.join(
            [".. WARNING: This file is autogenerated"
             ", do not edit it manually\n"] + content))


def generates_cli_help(rst_path):
    """
    Generate a reStructuredText file from Apyfal CLI '--help' commands.

    Args:
        rst_path (str): Path to ".rst" file
    """
    cli = [sys.executable or 'python3', '../accelpy/__main__.py']
    commands = (
        '', 'init', 'plan', 'apply', 'destroy', 'build', 'private_ip',
        'public_ip', 'ssh_user', 'ssh_private_key', 'list', 'lint')
    content = [
        'CLI',
        '====',
        '',
        'This section provides full CLI help (from ``--help``)',
        'for each command.',
        '']

    for command in commands:
        cli_help = check_output(
            cli + ([command, '-h'] if command else ['-h']),
            universal_newlines=True)
        title = 'accelpy%s' % ((' %s' % command) if command else '')
        content += [title, '-' * len(title), '\n| ' +
                    cli_help.replace('\n', '\n| '), '']

    # Save ".rst"
    _generates_rst(rst_path, content)


generates_cli_help('cli_help.rst')


# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon',
              'sphinx.ext.coverage', 'sphinx.ext.viewcode']
source_suffix = '.rst'
master_doc = 'index'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'default'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {'prev_next_buttons_location': None}
html_favicon = '_static/favicon.ico'
html_logo = '_static/logo.png'
html_show_sourcelink = False
html_show_sphinx = False
html_context = {'css_files': ['_static/accelize.css']}

# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = '%sdoc' % project


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
latex_documents = [(
    master_doc, '%s.tex' % project, '%s Documentation' % project, author,
    'manual')]


# -- Options for manual page output ------------------------------------------

man_pages = [(
    master_doc, PACKAGE_INFO['name'], '%s Documentation' % project,
    [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [(
    master_doc, project, '%s Documentation' % project, author, project,
    PACKAGE_INFO['description'], 'Miscellaneous')]
