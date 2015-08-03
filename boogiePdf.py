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
import pdfrw
import boogieInk

class BoogiePDFParser(object):
    def __init__(self,filename):
        self.filename = filename
        self.inkml_string = self.getInkML()
    def getInkML(self):
        r = pdfrw.PdfReader(self.filename)
        return r['/Root']['/Names']['/EmbeddedFiles']['/Names'][1]['/EF']['/F'].stream

    def parse(self, parser_class = boogieInk.BoogieInkParser, simple = False):
        self.inkml_parser = parser_class(self.inkml_string)
        self.inkml_parser.parse(simple)
        
        
