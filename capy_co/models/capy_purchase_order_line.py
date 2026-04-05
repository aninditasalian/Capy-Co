from odoo import models, fields, api

class CapyPurchaseOrderLine(models.Model):
    _name = "capy.purchase.order.line"
    _description = "List of the purchase orders made by CapyCo. An order can have multiple lines for the same order example: Line 1: 50 XL Capybara Plushie and Line 2: 100 small Capybara Plushies"

    product_id = fields.Many2one("capy.product", required = True)
    purchase_order_id = fields.Many2one("capy.purchase.order", required = True)
    quantity = fields.Integer(default = 1, required = True)
    unit_price = fields.Float(required = True)
    subtotal = fields.Float(compute = '_compute_subtotal')

    @api.depends("quantity", "unit_price")
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.cost