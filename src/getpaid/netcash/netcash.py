from Products.CMFCore.utils import getToolByName
from getpaid.core.options import PersistentOptions
from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility
from getpaid.netcash.interfaces import INetCashStandardProcessor, INetCashStandardOptions
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import implements
from zope.component import getUtility
from getpaid.core.interfaces import keys
import interfaces
import urllib
import urllib2
import sha

NetCashStandardOptions = PersistentOptions.wire("NetCashStandardOptions",
                                              "getpaid.netcash",
                                              interfaces.INetCashStandardOptions)


class NetCashStandardProcessor(object):
    """
    NetCash Standard Processor
    """
    implements(INetCashStandardProcessor)

    options_interface = INetCashStandardOptions

    def __init__(self, context):
        self.context = context

    def cart_post_button(self, cart):
        options = INetCashStandardOptions(self.context)

    def authorize(self, order, payment_information):
        """
        authorize an order, using payment information.
        """
        order_manager = getUtility(IOrderManager)
        order_manager.store(order)
        base_url = self.context.absolute_url()
        url = base_url + '/@@getpaid-netcash-redirect?orderid=%s' % (order.order_id)
        self.context.request.response.redirect(url)

    def capture(self, order, amount):
        """
        capture amount from order.
        """
        return keys.results_async

    def refund(self, order, amount):
        """
        reset
        """
