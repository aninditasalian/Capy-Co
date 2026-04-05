from odoo import models, fields, api

class CapyStock(models.Model):
    _name = "capy.stock"
    _description = "List of the Stock of the CapyCo Plushies"

    product_id = fields.Many2one("capy.product", required = True)
    quantity = fields.Integer(default = 0)
    min_quantity = fields.Integer(default = 10)
    max_quantity = fields.Integer(default = 100)
    location = fields.Char()
    last_updated = fields.Date(default = fields.Date.today) 
    stock_low = fields.Boolean(compute = '_compute_stock')

    @api.depends("quantity", "min_quantity")
    def _compute_stock(self):
        for record in self:
            if record.quantity< record.min_quantity:
                record.stock_low = True
            else:
                record.stock_low = False

