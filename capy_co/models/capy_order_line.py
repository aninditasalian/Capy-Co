from odoo import models, fields, api

class CapyOrderLine(models.Model):
    _name = "capy.order.line"
    _description = "List of the plushies. An order can have multiple lines for the same order example: Line 1: 1 XL Capybara Plushie and Line 2: 2 small Capybara Plushies"

    product_id = fields.Many2one("capy.product", required = True)
    order_id = fields.Many2one("capy.order", required = True)
    quantity = fields.Integer(default = 1, required = True)
    base_price = fields.Float(required = True)
    subtotal = fields.Float(compute = '_compute_subtotal')

    @api.depends("quantity", "base_price")
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.base_price