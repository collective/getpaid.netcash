from zope.app.locales.extract import find_files
#from zope.i18n.messageid import MessageID
from zope.i18nmessageid import Message
import xml.sax
from xml.sax.handler import feature_namespaces
from xml.sax.handler import ContentHandler
import traceback

def formulator_strings(dir, domain):
    catalog = {}
    for filename in find_files(dir, '*.form'):
        try:
            extract_ids(filename, catalog)
        except: # Hee hee, I love bare excepts!
            print 'There was an error processing', filename
            traceback.print_exc()
    return catalog

TRANSLATABLE_PROPERTIES = ['title', 'description']

class FormulatorXMLHandler(ContentHandler):
    def __init__(self, filepath, catalog):
        self._catalog = catalog
        self._tags = {}
        self._field_name = None
        self._i18n_domain = None
        self._stack = []
        self._locator = None
        self._filepath = filepath
        self._prev_characters = ''
        
    def setDocumentLocator(self, locator):
        self._locator = locator
        
    def isInTag(self, name):
        return self._tags.has_key((None, name))

    def processTranslatableProperty(self, chrs):
        if not (self.isInTag('field') and self.isInTag('values')):
            return
        name = self._stack[-1][1]
        if name not in TRANSLATABLE_PROPERTIES:
            return
        assert self._field_name is not None
        message_id = Message(chrs, self._i18n_domain)
        if not self._catalog.has_key(message_id):
            self._catalog[message_id] = []
        number = self._locator.getLineNumber()
        self._catalog[message_id].append((self._filepath, number))
        
    def enterTag(self, name):
        self._tags[name] = True
        self._stack.append(name)
        
    def exitTag(self, name):
        del self._tags[name]
        self._stack.pop()
        
    def startElementNS(self, name, qname, attrs):
        self.processCharacters()
        self.enterTag(name)
        
    def endElementNS(self, name, qname):
        self.processCharacters()
        self.exitTag(name)

    def processCharacters(self):
        if not self._prev_characters:
            return
        chrs = self._prev_characters
        self._prev_characters = ''
        if self.isInTag('i18n_domain'):
            self._i18n_domain = chrs
        elif self.isInTag('field') and self.isInTag('id'):
            self._field_name = chrs
        else:
            self.processTranslatableProperty(chrs)
        
    def characters(self, chrs):
        self._prev_characters += chrs
                    
def extract_ids(filename, catalog):
    handler = FormulatorXMLHandler(filename, catalog)
    parser = xml.sax.make_parser()
    parser.setFeature(feature_namespaces, 1)
    parser.setContentHandler(handler)
    handler.setDocumentLocator(parser)
    f = open(filename, 'r')
    parser.parse(f)
    f.close()
  
def main():
    catalog = {}
    extract_ids(
        '/home/faassen/working/instances27/Test273Zope/Products/Silva/views/add/File/form.form',
        catalog)
    for key, value in catalog.items():
        print key
        for v in value:
            print "  ",  v
        print
        
if __name__ == '__main__':
    main()
    
