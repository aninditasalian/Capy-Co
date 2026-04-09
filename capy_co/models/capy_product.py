from odoo import models, fields, api

class CapyProduct(models.Model):
    _name = "capy.product"
    _description = "Capybara Plushies"

    name = fields.Char(required=True)
    description = fields.Text()
    size = fields.Selection(selection =[('small', "Small"), ('medium', "Medium"), ('large', "Large"), ('xl', "XL")])
    price = fields.Float(required=True)
    _check_price = models.Constraint('CHECK(price>0)', 'Please check the price! The price cannot be less than zero.')
    cost = fields.Float(required=True)
    _check_cost = models.Constraint('CHECK(cost>0)', 'Please check the supplier cost again! The Cost from the supplier cannot be less than zero.')
    product_code = fields.Char()
    _unique_product_code = models.Constraint('UNIQUE(product_code)', 'All product codes must be unique.')
    image = fields.Image(string = 'productimage', max_width = 1024, max_height = 1024)
    active = fields.Boolean(default = True)
    profit_margin = fields.Float(compute = 'compute_profit_margin')
    
    @api.depends("price", "cost")
    def compute_profit_margin(self):
        for record in self:
            record.profit_margin = record.price - record.cost

    def action_create_order(self):
        return {'type': 'ir.actions.act_window',
        'name': 'new',
        'res_model': 'capy.order',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_order_line': [(0,0,{
                'product_id': self.id,
                'quantity': 1,
                'base_price': self.price,
                })]
            }
        }


    
