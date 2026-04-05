from odoo import models, fields, api 

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
    