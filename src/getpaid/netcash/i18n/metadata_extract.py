from zope.app.locales.extract import find_files
from zope.i18n.messageid import Message
import xml.sax
from xml.sax.handler import feature_namespaces
from xml.sax.handler import ContentHandler
import traceback

class NonMetadataXMLError(Exception):
    pass

def metadata_strings(dir, domain):
    catalog = {}
    # unfortunately since .xml is used for *both* silva export testfiles
    # *and* metadata descriptions, we get far too many files.
    # the handler tries to detect non metadata xml and bails out if so
    # as a hack
    for filename in find_files(dir, '*.xml'):
        try:
            try:
                extract_ids(filename, catalog, domain)
            except NonMetadataXMLError:
                pass
        except: # Hee hee, I love bare excepts!
            print 'There was an error processing', filename
            traceback.print_exc()
    return catalog

TRANSLATABLE_PROPERTIES = ['title', 'description']

class MetadataXMLHandler(ContentHandler):
    def __init__(self, filepath, catalog, i18n_domain):
        self._catalog = catalog
        self._tags = {}
        self._field_name = None
        self._stack = []
        self._attr_stack = []
        self._locator = None
        self._filepath = filepath
        self._i18n_domain = i18n_domain
        
    def setDocumentLocator(self, locator):
        self._locator = locator

    def isInTag(self, name):
        return self._tags.has_key((None, name))
    
    def enterTag(self, name, attrs):
        self._tags[name] = True
        self._stack.append(name)
        self._attr_stack.append(attrs)
        
    def exitTag(self, name):
        del self._tags[name]
        self._stack.pop()
        self._attr_stack.pop()

    def hasAttrValue(self, name, value):
        attrs = self._attr_stack[-1]
        return attrs.get((None, name)) == value

    def getAttrValue(self, name):
        return self._attr_stack[-1].get((None, name))
    
    def startElementNS(self, name, qname, attrs):
        self.enterTag(name, attrs)
        if not self.isInTag('metadata_set'):
            raise NonMetadataXMLError
        if self.isInTag('field_values') and self.isInTag('value'):
            for name in TRANSLATABLE_PROPERTIES:
                if self.hasAttrValue('key', name):
                    message_id = Message(self.getAttrValue('value'),
                                           self._i18n_domain)
                    if not self._catalog.has_key(message_id):
                        self._catalog[message_id] = []
                    number = self._locator.getLineNumber()
                    self._catalog[message_id].append((self._filepath, number))

    def endElementNS(self, name, qname):
        self.exitTag(name)
     
def extract_ids(filename, catalog, i18n_domain):
    handler = MetadataXMLHandler(filename, catalog, i18n_domain)
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
        '/home/faassen/working/instances27/Test273Zope/Products/Silva/doc/silva-extra.xml',
        catalog, 'silva')
    for key, value in catalog.items():
        print key
        for v in value:
            print "  ",  v
        print
        
if __name__ == '__main__':
    main()
    
