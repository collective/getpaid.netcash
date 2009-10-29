from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from getpaid.netcash.interfaces import INetCashStandardOptions
from zope.component import getUtility

class NetCashCheck(BrowserView):
    """
    A class which check
    """

    def __call__(self):
        """
        This takes the order Id and returns
        the XML to NetCash
        """
        orderId = self.request.orderID
        options = INetCashStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        netcashPrice = order.getTotalPrice()
        return '<orderid="%s" amount="%s" currency="%s">' % (order.getOrderId(),
                                                             netcashPrice,
                                                             currency)
