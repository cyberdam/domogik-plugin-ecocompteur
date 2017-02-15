import sys
import os

extensions = [
    'sphinx.ext.todo',
]

source_suffix = '.txt'

master_doc = 'index'

### part to update ###################################
project = u'domogik-plugin-ecocompteur'
copyright = u'2017, Cyberdam'
version = '1.0'
release = version
######################################################

pygments_style = 'sphinx'

html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = project

