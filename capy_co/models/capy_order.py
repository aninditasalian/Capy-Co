from odoo import models, fields, api

class CapyOrder(models.Model):
    _name = "capy.order"
    _description = "List of orders made by customers"

    name = fields.Char(required = True)
    customer_id = fields.Many2one('capy.customer', required = True)
    order_date = fields.Date(default = fields.Date.today)
    state = fields.Selection(selection = [('new', "New"), ('confirmed', "Confirmed"), ('shipped',"Shipped"), ('delivered', "Delivered"), ('cancelled', "Cancelled")], default = 'new')
    order_lines = fields.One2many('capy.order.line', 'order_id')
    total_amount = fields.Float(compute = "_compute_total_amount")

    @api.depends("order_lines.subtotal")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.order_lines.mapped('subtotal'))