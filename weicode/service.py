#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : weicode.py
# created at : 2013-05-07 11:25:03
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from flask import send_from_directory
from flask import render_template
from flask import request
from weicode.image import generate_image
from json import dumps as json_encode

from weicode import init, setting

app = init('conf/development.yaml')

@app.route('/static/<path:filename>')
def static(filename):
    return send_from_directory(setting['static_directory'], filename)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(setting['media_directory'], filename)


@app.route('/lang')
def lang():
    term = request.args.get('term', '')
    return json_encode(filter(lambda x: x.lower().startswith(term.lower()), setting['langs'].keys()))


@app.route('/', methods=['GET', 'POST'])
def start():
    # generate start page if we got a GET request
    if request.method == 'GET':
        return render_template('start.html',
                               setting=setting,
                               style='default',
                               langs=setting['langs'])
    elif request.method == 'POST':
        keys = ('lang', 'font_name', 'font_size', 'style', 'code')
        args = dict(map(lambda x: (x, request.form.get(x, '')), keys))
        args = validate(args)
        file_link, file_path = generate_image(args)
        return render_template('start.html',
                               setting=setting,
                               image_url=file_link,
                               **args)
    else:
        # bad request
        return 'bad request'


def validate(args):
    # tidy input
    if args['lang'] not in setting['langs'].keys():
        args['lang'] = 'Text only'

    if args['font_name'] not in setting['font_name']:
        args['font_name'] = setting['font_name'][0]

    if args['font_size'] not in setting['font_size']:
        args['font_size'] = setting['font_size'][0]

    if args['style'] not in setting['styles']:
        args['style'] = 'default'

    args['lexer'] = setting['langs'][args['lang']][0]

    print args
    return args

# vim: ts=4 sw=4 ai et st=4
