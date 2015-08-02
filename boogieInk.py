import xml.dom.minidom, re

class BoogiePen():
    def __init__(self):
        self.reset()
    def reset():
        self.coords = [0,0,0]
        self.velocity = [0,0,0]
        self.acceleration = [0,0,0]
        self.lastprefixes = ['!','!','!']
        

class BoogieInkParser():
    def __init__(self,ink_string):
        self.boogie_trace_point_regex = re.compile("\"?'?-?[0-9]+|\*")
        self.ink_string = ink_string
        self.trace_dom = xml.dom.minidom.parseString(self.ink_string)
        
    
    def parseTraceSimple(self):
        for trace_point in [re.findall(self.boogie_trace_point_regex, x.strip()) for x in self.trace_dom.childNodes[0].wholeText.split(',')]:
            self.simpleTracePointHandler(tracepoint)
            
    def parseTraceTracked(self):
        for trace_point in [re.findall(self.boogie_trace_point_regex, x.strip()) for x in self.trace_dom.childNodes[0].wholeText.split(',')]:
    #        print trace_point
            for i in [0,1,2]:
                if trace_point[i][0] in ['"',"'"]:
                    prefix = trace_point[i][0]
                    states.pen.lastprefixes[i] = prefix
                    numoffset=1
                else:
                    if trace_point[i][0] == '*':
                        last_state=True
                    else:
                        last_state=False
                    prefix = self.pen.lastprefixes[i]
                    numoffset=0
    
                if prefix == '"' and not last_state:
                    states.pen.acceleration[i] = int(trace_point[i][numoffset:].strip())
    
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
    
            self.trackedTracePointHandler(self.pen.coords)
            
    
    def parse(self,simple = False):
        traceHandler = self.parseTraceSimple if simple else self.parseTraceTracked

        self.InfoHandler(self.trace_dom.getElementsByTagNameNS('http://www.w3.org/2003/InkML','channel'))
    
        for trace in self.trace_dom.getElementsByTagNameNS('http://www.w3.org/2003/InkML','trace'):
            self.pen.reset()
            self.traceBeginHandler()
            traceHandler()
            self.traceEndHandler()

    def traceBeginHandler(self):
        pass
    
    def simpleTracePointHandler(self):
        pass

    def trackedTracePointHandler(self):
        pass

    def traceEndHandler(self):
        pass
