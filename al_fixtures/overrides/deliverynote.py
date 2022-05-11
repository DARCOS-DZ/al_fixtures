from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from al_fixtures.controllers.selling_controller import CustomSellingController

class CustomDeliveryNote(DeliveryNote, CustomSellingController):
    pass
