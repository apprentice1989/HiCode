#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : image.py
# created at : 2013-05-08 12:57:48
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from hicode import setting
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name

from cStringIO import StringIO
from os.path import dirname, exists, join as path_join
from os import makedirs
import hashlib
import time
import Image
import ImageEnhance



def generate_image(args):
    # do format
    lexer = get_lexer_by_name(args['lexer'], stripall=True)
    formatter = ImageFormatter(image_format='png',
                               font_name=args['font_name'],
                               font_size=args['font_size'],
                               style=args['style'],
                               line_number_chars=3,
                               image_pad=24,
                               linenos=True)
    ## generate formatted image
    result = highlight(args['code'], lexer, formatter)
    file_link, file_path = get_image_path(args)

    # attach watermark
    image = Image.open(StringIO(result))
    mark = Image.open(setting['watermark'])
    mark_pos = (image.size[0] - mark.size[0], 0)
    out = watermark(image, mark, mark_pos, 0.5)

    # make directories if not exist
    if not exists(dirname(file_path)):
        makedirs(dirname(file_path))

    # write file to disk
    out.save(file_path)

    return file_link, file_path


def get_image_path(args, extension='.png'):
    # find a place for saving the image
    level1 = time.strftime('%Y-%m-%d')
    level2 = time.strftime('%H-%M-%S')
    level3 = hashlib.md5(args['code']).hexdigest() + extension

    file_path = path_join(setting['media_directory'],
                          level1, level2, level3)
    file_link = path_join(setting['site_url'], 'media',
                          level1, level2, level3)

    return file_link, file_path



def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)
