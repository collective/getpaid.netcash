from getpaid.netcash import _
from zope.schema import vocabulary

def serverUrlsChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [(_("Production Server"), u"https://gateway.netcash.co.za/vvonline/ccnetcash.asp"),])

def currencyChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [(_(u"SOUTH AFRICAN RAND"), u"zar")])

def budgetChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [(_(u"Yes"), u"yes"), (_(u"No"), u"no")])
