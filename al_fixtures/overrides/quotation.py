from erpnext.selling.doctype.quotation.quotation import Quotation
from al_fixtures.controllers.selling_controller import CustomSellingController

class CustomQuotation(Quotation, CustomSellingController):
    pass
