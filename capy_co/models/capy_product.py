from odoo import models, fields

class CapyProduct(models.Model):
    _name = "capy.product"
    _description = "Capybara Plushies"

    name = fields.Char(required=True)
    price = fields.Float(required=True)
    stock = fields.Integer()
