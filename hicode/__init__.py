#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : __init__.py
# created at : 2013-05-08 13:03:43
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from flask import Flask
from yaml import load as yaml_load
from jinja2.loaders import FileSystemLoader

setting = yaml_load("""
---
site_url: http://localhost:5000/
static_directory: ../static
media_directory: ../media
template_directory: template
watermark: static/watermark.png
debug: True
font_name:
  - 'Monofur'
  - 'DejaVu Sans Mono'
  - 'Droid Sans Mono'
  - 'Consolas'
  - 'Bitstream Vera Sans Mono'
font_size:
  - '11'
  - '12'
  - '13'
  - '14'
  - '15'
  - '18'
  - '22'
  - '24'
  - '32'
""")

def init(cfg):
    from yaml import load as yaml_load
    from jinja2 import FileSystemLoader
    from os.path import join as path_join, exists
    from hicode import setting
    from pygments.lexers import get_all_lexers
    from pygments.styles import get_all_styles

    if exists(cfg):
        users = yaml_load(file(cfg).read())
        setting.update(users)

    setting['styles'] = list(get_all_styles())
    setting['langs'] = dict(map(lambda x: (x[0], x[1]), get_all_lexers()))

    app = Flask('hicode')
    app.jinja_loader = FileSystemLoader(setting['template_directory'])
    app.debug = setting['debug']

    return app
