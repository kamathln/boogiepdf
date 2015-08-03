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

import boogiePdf, boogieInk
import sys

class BoogieInkTracePrinter(boogieInk.BoogieInkParser):
    def __init__(self, inkstring):
        super(BoogieInkTracePrinter, self).__init__(inkstring)
        self.trace_counter=0
        self.total_tracepointer_counter = 1

    def traceBeginHandler(self,trace):
        self.trace_counter += 1
        self.tracepoint_counter = 0
        print ("Trace #{0} begins".format(self.trace_counter))

    def trackedTracePointHandler(self,trace,trace_point,trace_len):
        self.tracepoint_counter +=1
        print ("X: {0}, Y:{1}, Pressure: {2}".format (*trace_point))

    def simpleTracePointHandler(self,trace,trace_point,trace_len):
        self.tracepoint_counter +=1
        xyf='XYF'

        info='['
        for i in [0,1,2]:
            if trace_point[i][0] in ['"',"'"]:
                prefix = trace_point[i][0]
                self.pen.lastprefixes[i] = prefix
                last_state=False
                numoffset=1
            else:
                if trace_point[i][0] == '*':
                    last_state=True
                    info+= "Repeating Previous action for "+xyf[i]+','
                else:
                    last_state=False
                prefix = self.pen.lastprefixes[i]
                numoffset=0
    
            if prefix == '"' and not last_state:
                info += "Setting acceleration of {0} to {1},".format(xyf[i], trace_point[i][numoffset:].strip())
    
            if prefix == "'" and not last_state:
                info += "Setting velocity of {0} to {1},".format(xyf[i], trace_point[i][numoffset:].strip())
    
            if prefix == '!' and not last_state:
                info += "Setting position of {0} to {1},".format(xyf[i], trace_point[i][numoffset:].strip())
        info += ']'
        print (info)

    def traceEndHandler(self,trace):
        self.total_tracepointer_counter += self.tracepoint_counter
        print ("Trace #{0} ends with {1} points".format(self.trace_counter, self.tracepoint_counter))
    
    def infoHandler(self,info):
        print ("""Info: MaxX:{X} MaxY:{Y} MaxPressure:{F}""".format(**info))

    def parseEndHandler(self):
        print ("""Parsing ends

Statistics:
==========
Total traces {0}
Total trace points {1}""".format(self.trace_counter, self.total_tracepointer_counter)
)


if __name__ == "__main__":
    parser = boogiePdf.BoogiePDFParser(sys.argv[1])
    parser.parse(BoogieInkTracePrinter,simple=True)


