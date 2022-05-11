from erpnext.crm.doctype.lead.lead import Lead
from al_fixtures.controllers.selling_controller import CustomSellingController

class CustomLead(Lead, CustomSellingController):
    pass
