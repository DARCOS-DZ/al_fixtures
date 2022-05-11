from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from al_fixtures.controllers.selling_controller import CustomSellingController

class CustomSalesOrder(SalesOrder, CustomSellingController):
    pass
