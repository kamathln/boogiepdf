# Copyright (c) 2015 Laxmianarayan G Kamath A kamathln@gmail.com
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import xml.dom.minidom, re

class BoogiePen(object):
    """ Simple class used by BoogieInkParser to maintain pen state """
    def __init__(self):
        self.reset()
    def reset(self):
        self.coords = [0,0,0]
        self.velocity = [0,0,0]
        self.acceleration = [0,0,0]
        self.lastprefixes = ['!','!','!']
        

class BoogieInkParser(object):
    """ Ink Parser class.  """
    def __init__(self,ink_string, **kwargs):
        self.kwargs = kwargs
        self.boogie_trace_point_regex = re.compile("\"?'?-?[0-9]+|\*")
        self.ink_string = ink_string
        self.ink_dom = xml.dom.minidom.parseString(self.ink_string)
        self.pen = BoogiePen()
        self.numof_traces = len(self.ink_dom.getElementsByTagNameNS('http://www.w3.org/2003/InkML','trace')) 
        
    def parseTraceSimple(self,trace_dom):
        trace_points = [re.findall(self.boogie_trace_point_regex, x.strip()) for x in trace_dom.childNodes[0].wholeText.split(',')]
        trace_points_len = len(trace_points)
        for trace_point in trace_points:
            self.simpleTracePointHandler(trace_dom,trace_point,trace_points_len)
            
    def parseTraceTracked(self,trace_dom):
        trace_points = [re.findall(self.boogie_trace_point_regex, x.strip()) for x in trace_dom.childNodes[0].wholeText.split(',')]
        trace_points_len = len(trace_points)
        for trace_point in trace_points:
    #        print trace_point
            for i in [0,1,2]:
                if trace_point[i][0] in ['"',"'"]:
                    prefix = trace_point[i][0]
                    self.pen.lastprefixes[i] = prefix
                    numoffset=1
                else:
                    if trace_point[i][0] == '*':
                        last_state=True
                    else:
                        last_state=False
                    prefix = self.pen.lastprefixes[i]
                    numoffset=0
    
                if prefix == '"' and not last_state:
                    self.pen.acceleration[i] = int(trace_point[i][numoffset:].strip())
    
                if prefix == "'":
                    if not last_state:
                        self.pen.velocity[i] = int(trace_point[i][numoffset:].strip())
                else:
                    self.pen.velocity[i] += self.pen.acceleration[i]
    
                if prefix == '!':
                    if not last_state:
                        self.pen.coords[i] = int(trace_point[i][numoffset:].strip())
                else:
                    self.pen.coords[i] += self.pen.velocity[i]
    
            self.trackedTracePointHandler(trace_dom,self.pen.coords,trace_points_len)
            
    
    def parse(self,simple = False):
        traceHandler = self.parseTraceSimple if simple else self.parseTraceTracked

        self.infoHandler(
            dict([(chan.getAttribute('name'),int(chan.getAttribute('max'))) for chan in 
                self.ink_dom.getElementsByTagNameNS('http://www.w3.org/2003/InkML','channel')])
        )

        for trace in self.ink_dom.getElementsByTagNameNS('http://www.w3.org/2003/InkML','trace'):
            self.pen.reset()
            self.traceBeginHandler(trace)
            traceHandler(trace)
            self.traceEndHandler(trace)
        self.parseEndHandler()

    def infoHandler(self, info):
        pass

    def traceBeginHandler(self,trace):
        pass
    
    def simpleTracePointHandler(self,trace,trace_point,trace_len):
        pass

    def trackedTracePointHandler(self,trace,trace_point,trace_len):
        pass

    def traceEndHandler(self,trace):
        pass

    def parseEndHandler(self):
        pass
