#!/usr/bin/python

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/svg2tikz')

from svg2tikz.extensions.tikz_export import convert_svg
from subprocess import Popen
import logging

config = {'images': os.getcwd() + '/images',
          'texfile': 'sw_dev_process.tex'}


def gen_images(imgpath):
    files = [imgpath + '/' + f for f in os.listdir(imgpath)
             if f.endswith('.svg')]
    for fname in files:
        texname = fname.replace('.svg', '.tex')
        with open(texname, 'w') as fout:
            fout.write(convert_svg(fname, codeoutput='figonly'))


def gen_images2(imgpath):
    # inkscape -z -D -e Scrum_process.png Scrum_process.svg
    files = [imgpath + '/' + f for f in os.listdir(imgpath)
             if f.endswith('.svg')]
    process = [f for f in files
               if (
                   not os.path.isfile(f.replace('.svg', '.png'))
                   or os.path.getmtime(f.replace('.svg', '.png'))
                   < os.path.getmtime(f)
               )]
    for f in process:
        inkscape = Popen(['inkscape', '-z', '-D', '-e',
                          f.replace('.svg', '.png'), f])
        inkscape.communicate()


def compile_pdf(texfile):
    proc = Popen(['pdflatex', texfile])
    proc.communicate()
    proc = Popen(['pdflatex', texfile])
    proc.communicate()


def cleanup(texfile, imgpath):
    os.unlink(texfile.replace('.tex', '.aux'))
    os.unlink(texfile.replace('.tex', '.log'))
    [os.unlink(imgpath + '/' + f)
     for f in os.listdir(imgpath)
     if f.endswith('.tex')]


def main():
    if not os.path.exists(config['texfile']):
        logging.error("Can't find TeX input %s" % config['texfile'])
        return
    if not os.path.exists(config['images']):
        logging.warning('Image directory %s is not accessible'
                        % config['images'])
    else:
        gen_images2(config['images'])
    compile_pdf(config['texfile'])
    cleanup(config['texfile'], config['images'])


if __name__ == '__main__':
    main()
