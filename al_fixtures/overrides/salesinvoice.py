from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from al_fixtures.controllers.selling_controller import CustomSellingController

class CustomSalesInvoice(SalesInvoice, CustomSellingController):
    pass
