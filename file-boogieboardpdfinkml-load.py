#!/usr/bin/env python

# GIMP Plug-in for opening InkML from BoogieBoard PDF

# Copyright (C) 2012 by Laxminarayan G Kamath A <kamathln@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#

from gimpfu import *

import boogiePdf, boogieInk

class BoogieInkGimpLoader(boogieInk.BoogieInkParser):

    def infoHandler(self, info):
        self.image_scale = 0.2
        self.xMax = int(int(info['X']) * self.image_scale)
        self.yMax = int(int(info['Y']) * self.image_scale)
        self.pressureMax = int(info['F'])
        self.pressureMultiplier = 1/self.pressureMax
        print ("pressureMax",self.pressureMultiplier, self.pressureMax)
        self.gimp_image = gimp.Image(self.xMax, self.yMax, RGB)
        self.draw_layer = gimp.Layer(self.gimp_image, 'canvas', self.xMax, self.yMax)
        self.gimp_image.insert_layer(self.draw_layer)
        self.draw_layer.fill(1)
        pdb['gimp-context-set-paint-method']('gimp-paintbrush')
        self.orig_brush_size = pdb['gimp-context-get-brush-size']()


    def traceBeginHandler(self,trace):
        print "setting last point to none"
        self.last_point=None

    def trackedTracePointHandler(self, trace, trace_point):
        point = [int(trace_point[0] * self.image_scale),int(trace_point[1] * self.image_scale)]
        pdb['gimp-context-set-brush-size'](1 + (self.orig_brush_size * (float(trace_point[2])/float(self.pressureMax)))) 
        if self.last_point:
            pdb['gimp-paintbrush-default'](self.draw_layer,4,self.last_point + point)
        else:
            pdb['gimp-paintbrush-default'](self.draw_layer,2,point)
        self.last_point = point

def load_boogiepdf(filename, raw_filename):
    boogie_pdf_parser = boogiePdf.BoogiePDFParser(filename) 
    boogie_pdf_parser.parse(parser_class = BoogieInkGimpLoader)
    boogie_pdf_parser.inkml_parser.gimp_image.filename = filename

    return boogie_pdf_parser.inkml_parser.gimp_image


def register_load_handlers():
    gimp.register_load_handler('file-boogieboardpdfinkml-load', 'pdf', '')
    pdb['gimp-register-file-handler-mime']('file-boogieboardpdfinkml-load', 'application/pdf')



register(
    'file-boogieboardpdfinkml-load', #name
    'load inkml from a BoogieBoard PDF', #description
    'load inkml from a BoogieBoard PDF',
    'Laxminarayan Kamath <kamathln@gmail.com>', #author
    'Laxminarayan Kamath <kamathln@gmail.com>', #copyright
    '2012', #year
    'BoogieBoard PDF InkML',
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_STRING, 'raw-filename', 'The name entered', None),
    ],
    [(PF_IMAGE, 'image', 'Output image')], #results. Format (type, name, description)
    load_boogiepdf, #callback
    on_query = register_load_handlers,
    menu = "<Load>",
)


main()
