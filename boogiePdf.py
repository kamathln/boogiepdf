import pdfrw
import boogieInk

class BoogiePDFParser(object):
    def __init__(self,filename):
        self.filename = filename
        self.inkml_string = self.getInkML()
    def getInkML(self):
        return pdfrw.PdfReader(self.filename)['/Root']['/Names']['/EmbeddedFiles']['/Names'][1]['/EF']['/F'].stream

    def parse(self, parser_class = boogieInk.BoogieInkParser, simple = False):
        self.inkml_parser = parser_class(self.inkml_string)
        self.inkml_parser.parse(simple)
        
        
