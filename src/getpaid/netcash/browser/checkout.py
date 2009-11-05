import decimal,operator
import cgi
from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay, sanitize_custom_widgets, null_condition
from Products.PloneGetPaid.browser.checkout import CheckoutController as OriginalCheckoutController
from getpaid.core import interfaces, options
from getpaid.core.interfaces import IPaymentProcessor
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from zope import component
from zope import schema
from zope.component import getAdapter
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from getpaid.wizard import Wizard, ListViewController, interfaces as wizard_interfaces
from getpaid.wizard import interfaces as wizard_interfaces

class NetCashCheckoutPayment(CheckoutReviewAndPay):
    """
    We need to override some of the method for the checkout
    as the checkout process is different for NetCash
    """
##    #form_fields = form.FormFields
##    @property
##    def form_fields(self):
##        fields = getattr(self,'__form_fields',None)
##        if fields:
##            return fields
##        args = []
##        formSchemas = CheckoutReviewAndPay.component.getUtility(interfaces.IFormSchemas)
##        for section in self.sections:
##            args.append(formSchemas.getInterface(section))
##        fields = form.Fields(*args)
##        customise_widgets = getattr(self,'customise_widgets',None)
##        if customise_widgets is not None:
##            customise_widgets(fields)
##        self.__form_fields = fields
##        return fields
    
    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")

##    def setUpWidgets( self, ignore_request=False ):
##        self.adapters = self.adapters is not None and self.adapters or {}
##        
##        # grab all the adapters and fields from the entire wizard form sequence (till the current step)
##        adapters = self.wizard.data_manager.adapters
##        fields   = self.wizard.data_manager.fields
##        
##        formSchemas = component.getUtility(interfaces.IFormSchemas)
##        # edit widgets for payment info
##        self.widgets = form.setUpEditWidgets(
##            self.form_fields.select( *schema.getFieldNames(formSchemas.getInterface('payment'))),
##            self.prefix, self.context, self.request,
##            adapters=adapters, ignore_request=ignore_request
##            )
##        
##        # display widgets for bill/ship address
##        bill_ship_fields = []
##        for i in (formSchemas.getInterface('billing_address'),
##                  formSchemas.getInterface('shipping_address')):
##            bill_ship_fields.append(fields.select(*schema.getFieldNamesInOrder(i)))
##        # make copies of custom widgets.. (typically for edit, we want display)
##        bill_ship_fields = sanitize_custom_widgets(
##            reduce(operator.__add__,bill_ship_fields)
##            )
##        
##        self.widgets += form.setUpEditWidgets(
##            bill_ship_fields,  self.prefix, self.context, self.request,
##            adapters=adapters, for_display=True, ignore_request=ignore_request
##            )

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}

        # grab all the adapters and fields from the entire wizard form
        # sequence (till the current step)
        adapters = self.wizard.data_manager.adapters
        fields   = self.wizard.data_manager.fields

        # display widgets for bill/ship address
        bill_ship_fields = []
        form_schemas = component.getUtility(
            interfaces.IFormSchemas)
        for i in (form_schemas.getInterface('billing_address'),
                  form_schemas.getInterface('shipping_address')):
            bill_ship_fields.append(fields.select(*schema.getFieldNamesInOrder(i)))
        # make copies of custom widgets.. (typically for edit, we want display)
        bill_ship_fields = sanitize_custom_widgets(
            reduce(operator.__add__,bill_ship_fields)
            )

        self.widgets = form.setUpEditWidgets(
            bill_ship_fields,  self.prefix, self.context, self.request,
            adapters=adapters, for_display=True, ignore_request=ignore_request
            )


    @form.action(u"Make Payment", name="make-payment")
    def makePayment(self, action, data):
        """ create an order, and submit to the processor
        """
        manage_options = IGetPaidManagementOptions( self.context )
        processor_name = manage_options.payment_processor

        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )

        processor = component.getAdapter( self.context,
                                IPaymentProcessor,
                                processor_name )
        ##self.extractData( data )

        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )
        order_manager = component.getUtility( interfaces.IOrderManager )
##        order_manager.store( order )
        
        result = processor.authorize( order, None )


