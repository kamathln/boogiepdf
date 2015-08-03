import xml.dom.minidom
import sys, os
import boogiePdf, boogieInk
import copy


class BoogiInkToKritaRec(boogieInk.BoogieInkParser):
    
    def tmplput(self, tmplpart):
        sys.stdout.write(tmplpart)
    
    def gettmpl(self, templatename):
        return open(self.basepath+ '/dom_templates/' + templatename + '.tmpl').read()
    
    def infoHandler(self, info):
        self.basepath = os.path.normpath(os.path.dirname(__file__))
        self.image_scale = 0.3
        self.xMax = int(int(info['X']) * self.image_scale)
        self.yMax = int(int(info['Y']) * self.image_scale)
        self.pressureMax = float(info['F']  / 7.0)

        self.tmplput(self.gettmpl('top_head'))
        self.linetemplate = self.gettmpl('line')
        self.pointtemplate = self.gettmpl('point')

        self.parse_done = False
        self.counter = 0

    def traceBeginHandler(self,trace):
        self.tmplput(self.gettmpl('recordedaction_head'))
        self.previous_point = None

    def trackedTracePointHandler(self, trace, trace_point, trace_length):
        line_dom = xml.dom.minidom.Element('Line')
        self.counter += 20
        if trace_length >= 2:
            if self.previous_point is not None:
                self.tmplput(self.linetemplate.format(
                 self.previous_point[0] * self.image_scale
                 ,self.previous_point[1] * self.image_scale
                 ,"%.3f" % (self.previous_point[2]/self.pressureMax)
                 ,self.counter
                 ,trace_point[0] * self.image_scale
                 ,trace_point[1] * self.image_scale
                 ,"%.3f" % (trace_point[2]/self.pressureMax)
                 ,self.counter + 10
                 )
                )
            self.previous_point = copy.copy(trace_point)
        elif trace_length == 1:
            self.tmplput(self.pointtemplate.format(
             trace_point[0] * self.image_scale
             ,trace_point[1] * self.image_scale
             ,"%.3f" % (trace_point[2]/self.pressureMax)
             ,self.counter
             )
            )

    def traceEndHandler(self,trace):
        self.tmplput (self.gettmpl('recordedaction_tail'))

    def parseEndHandler(self):
        self.tmplput (self.gettmpl('top_tail'))
        self.parse_done = True

            


if __name__ == '__main__':
    pdfParser = boogiePdf.BoogiePDFParser(sys.argv[1])
    pdfParser.parse(parser_class=BoogiInkToKritaRec)
