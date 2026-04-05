from odoo import models, fields, api

class CapyPurchaseOrder(models.Model):
    _name = "capy.purchase.order"
    _description = "List of the purchase orders given by CapyCo to restock the Capybara plushies"

    name = fields.Char(required = True)
    supplier_id = fields.Many2one("capy.supplier", required = True)
    order_date = fields.Date(default = fields.Date.today)
    expected_date = fields.Date()
    state = fields.Selection(selection = [('draft', "Draft"), ('confirmed', "Confirmed"), ('received', "Received"), ('cancelled', "Cancelled")], default = 'draft')
    order_lines = fields.One2many("capy.purchase.order.line", "purchase_order_id")
    total_cost = fields.Float(compute = "_compute_total_cost")
    notes = fields.Text()

    @api.depends("order_lines.subtotal")
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(record.order_lines.mapped('subtotal'))
    