from odoo import models, api

class SaleOrderInherit(models.Model):
    _inherit = ['sale.order']

    @api.model
    def action_confirm(self):
        print("invoices\n\n\n=======================================================================")
        for order in self:
            order.with_delay().action_confirm()