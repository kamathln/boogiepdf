import xml.dom.minidom, re

class BoogiePen(object):
    def __init__(self):
        self.reset()
    def reset(self):
        self.coords = [0,0,0]
        self.velocity = [0,0,0]
        self.acceleration = [0,0,0]
        self.lastprefixes = ['!','!','!']
        

class BoogieInkParser(object):
    def __init__(self,ink_string):
        self.boogie_trace_point_regex = re.compile("\"?'?-?[0-9]+|\*")
        self.ink_string = ink_string
        self.ink_dom = xml.dom.minidom.parseString(self.ink_string)
        self.pen = BoogiePen()
        
    
    def parseTraceSimple(self,trace_dom):
        for trace_point in [re.findall(self.boogie_trace_point_regex, x.strip()) for x in trace_dom.childNodes[0].wholeText.split(',')]:
            self.simpleTracePointHandler(tracepoint)
            
    def parseTraceTracked(self,trace_dom):
        for trace_point in [re.findall(self.boogie_trace_point_regex, x.strip()) for x in trace_dom.childNodes[0].wholeText.split(',')]:
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
    
            self.trackedTracePointHandler(trace_dom,self.pen.coords)
            
    
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
    
    def simpleTracePointHandler(self,trace):
        pass

    def trackedTracePointHandler(self,trace,trace_point):
        pass

    def traceEndHandler(self,trace):
        pass

    def parseEndHandler(self):
        pass
