from getpaid.core import interfaces
from zope import schema
from getpaid.netcash import _


class INetCashStandardOptions(interfaces.IPaymentProcessorOptions):
    """
    NetCash Standard Options
    """
    server_url = schema.Choice(title = _(u"NetCash Website Payments Server"),
                               vocabulary = "getpaid.netcash.server_urls")

    ncusername = schema.ASCIILine(
        description = _(u"This is your NetCash assigned electronic Username"),
        required = True,
        title = _(u"NetCash Username"))
    
    ncpassword = schema.ASCIILine(
        description = _(u"This is your NetCash assigned electronic Password"),
        required = True,
        title = _(u"NetCash Password"))
    
    ncpin = schema.ASCIILine(
        description = _(u"This is your NetCash assigned electronic PIN"),
        required = True,
        title = _(u"NetCash PIN"))
    
    ncid = schema.ASCIILine(
        description = _(u"This is your Terminal Number"),
        required = True,
        title = _(u"NetCash Terminal Number"))

    orderdesc = schema.TextLine(
        description = _(u"This is the description for all orders from your shop"),
        required = True,
        title = _(u"Description of Goods"))

    currency = schema.Choice(
        title = _(u"Currency"),
        vocabulary = "getpaid.netcash.currencies")
    
    budget = schema.Choice(
        title= _(u"Allow Budget transactions"),
        vocabulary = "getpaid.netcash.budget")

class INetCashStandardProcessor(interfaces.IPaymentProcessor):
    """
    VCS Standard Processor
    """
