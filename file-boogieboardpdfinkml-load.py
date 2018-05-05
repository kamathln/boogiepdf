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
import sys

class BoogieInkGimpLoader(boogieInk.BoogieInkParser):

    def infoHandler(self, info):
        self.image_scale = 0.3
        self.xMax = int(int(info['X']) * self.image_scale)
        self.yMax = int(int(info['Y']) * self.image_scale)
        self.pressureMax = float(info['F'])
        self.pressureMultiplier = 1/self.pressureMax
        self.gimp_image = gimp.Image(self.xMax, self.yMax, RGB)
        self.draw_layer = gimp.Layer(self.gimp_image, 'canvas', self.xMax, self.yMax)
        self.gimp_image.insert_layer(self.draw_layer)
        self.draw_layer.fill(1)
        pdb['gimp-context-set-paint-method']('gimp-paintbrush')
        self.orig_brush_size = pdb['gimp-context-get-brush-size']()
        self.sbs = pdb['gimp-context-set-brush-size']
        self.pb  = pdb['gimp-paintbrush-default']
        self.so  = pdb['gimp-context-set-opacity']
        self.orig_opacity = pdb['gimp-context-get-opacity']()
        self.trace_counter = 0

    def traceBeginHandler(self,trace):
        self.trace_counter += 1
        pdb.gimp_progress_update(float(self.trace_counter)/float(self.numof_traces))
        pdb.gimp_progress_set_text("Importing trace #{0} of #{1}".format(self.trace_counter,self.numof_traces))
        pdb.gimp_progress_update(float(self.trace_counter)/float(self.numof_traces))

        self.previous_point = None
        self.points = []

    def trackedTracePointHandler(self, trace, trace_point,trace_len):
        point = [int(trace_point[0] * self.image_scale),int(trace_point[1] * self.image_scale)]
        #pressure = float(self.trace_point[2]) * self.kwargs['pressure_multiplier']
        pressure = float(trace_point[2]) * float(self.pressureMultiplier) * 1024.0 * float(self.kwargs['pressure_multiplier'])
        self.sbs(1 + (self.orig_brush_size * (pressure/float(self.pressureMax)))) 
        o = float(pressure) * 0.09765625
        self.so(o if 0 <= o <= 100  else 100 )
        if self.previous_point:
            self.pb(self.draw_layer,4,self.previous_point + point)
        else:
            self.pb(self.draw_layer,2,point)
        self.previous_point = point

    def parseEndHandler(self):
        self.so(self.orig_opacity)
        self.sbs(self.orig_brush_size)

    def traceEndHandler(self,trace):
        self.so(self.orig_opacity)
        self.sbs(self.orig_brush_size)

class BoogieInkGimpLoaderSimple(BoogieInkGimpLoader):
    def trackedTracePointHandler(self, trace, trace_point,trace_len):
        self.points.extend([int(trace_point[0] * self.image_scale),int(trace_point[1] * self.image_scale)])

    def traceEndHandler(self, trace):
        self.pb(self.draw_layer,len(self.points),self.points)
    

def load_boogiepdf(filename, raw_filename, skipped_param, skip_import_pressure, pressure_multiplier):
    try:
        boogie_pdf_parser = boogiePdf.BoogiePDFParser(filename) 
        if skip_import_pressure:
            boogie_pdf_parser.parse(parser_class = BoogieInkGimpLoaderSimple)
        else:
            boogie_pdf_parser.parse(parser_class = BoogieInkGimpLoader, pressure_multiplier=pressure_multiplier)
        boogie_pdf_parser.inkml_parser.gimp_image.filename = filename

        return boogie_pdf_parser.inkml_parser.gimp_image
    except Exception as e:
        pdb.gimp_progress_end()
        raise e


def register_load_handlers():
    gimp.register_load_handler('file-boogieboardpdfinkml-load', 'pdf', '')
    pdb['gimp-register-file-handler-mime']('file-boogieboardpdfinkml-load', 'application/pdf')



register(
    'file-boogieboardpdfinkml-load', #name
    'load inkml from a BoogieBoard PDF', #description
    'load inkml from a BoogieBoard PDF',
    'Laxminarayan Kamath <kamathln@gmail.com>', #author
    'Laxminarayan Kamath <kamathln@gmail.com>', #copyright
    '2015', #year
    'BoogieBoard PDF InkML',
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_STRING, 'raw-filename', 'The name entered', None),
        (PF_BOOL,'skipped_param', 'skipped_param',None),
        (PF_BOOL,'skip_import_pressure', 'skip import pressure(fast)',True),
        (PF_SPINNER,'pressure_multiplier', 'Pressure multiplier',1.0, [0.0, 100.0, 0.01]),
       # (PF_BOOL,'run_type', 'Interact',True),
    ],
    [(PF_IMAGE, 'image', 'Output image')], #results. Format (type, name, description)
    load_boogiepdf, #callback
    on_query = register_load_handlers,
    menu = "<Load>",
)


main()
