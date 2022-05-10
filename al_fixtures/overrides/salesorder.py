from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

class CustomSalesOrder(SalesOrder):
    def set_total_in_words(self):
        from al_fixtures.utils.data import money_in_words
        if self.meta.get_field("base_in_words"):
            base_amount = abs(
            self.base_grand_total if self.is_rounded_total_disabled() else self.base_rounded_total
            )
            self.base_in_words = money_in_words(base_amount, self.company_currency)

        if self.meta.get_field("in_words"):
            amount = abs(self.grand_total if self.is_rounded_total_disabled() else self.rounded_total)
            self.in_words = money_in_words(amount, self.currency)