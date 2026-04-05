from odoo import models, fields, api
from datetime import timedelta

class CapyPayment(models.Model):
    _name = "capy.payment"
    _description = "List of payments made by customers"

    name = fields.Char(required = True)
    customer_id = fields.Many2one("capy.customer", required = True)
    invoice_id = fields.Many2one("capy.invoice", required = True)
    payment_date = fields.Date(default = fields.Date.today)
    amount = fields.Float(default = 0.0, required = True)
    payment_method = fields.Selection(selection = [('cash', "Cash on Delivery"), ('card', "Card")], default = 'card')
    state = fields.Selection(selection = [('confirmed', "Confirmed"), ('failed', "Failed"), ('pending', "Pending"), ('refunded', "Refunded")], default = 'pending')
    
    def write(self, var):
        rec = super().write(var)
        if vals.get('state') == 'confirmed':
            for record in self:
                self.env["capy.invoice"].create({
                    'name': 'INV-' + record.name,
                    'customer_id': record.customer_id.id,
                    'order_id': record.invoice_id.order_id.id,
                    'invoice_date': fields.Date.today,
                    'due_date': fields.Date.today + timedelta(days=15),
                    'amount_paid': record.amount,
                    'state': 'draft',
                })
        return rec
    
    