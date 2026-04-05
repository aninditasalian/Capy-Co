from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class CapyOrder(models.Model):
    _name = "capy.order"
    _description = "List of orders made by customers"

    name = fields.Char(required = True)
    customer_id = fields.Many2one('capy.customer', required = True)
    order_date = fields.Date(default = fields.Date.today)
    state = fields.Selection(selection = [('new', "New"), ('confirmed', "Confirmed"), ('shipped',"Shipped"), ('delivered', "Delivered"), ('cancelled', "Cancelled")], default = 'new', readonly=True)
    order_lines = fields.One2many('capy.order.line', 'order_id')
    total_amount = fields.Float(compute = "_compute_total_amount", store=True, group_operator="sum")
    notes = fields.Text()
    total_margin = fields.Float(compute="_compute_total_margin", store=True, string="Total Profit")

    @api.depends("order_lines.subtotal")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.order_lines.mapped('subtotal'))

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_ship(self):
        for record in self:
            record.state = 'shipped'

    def action_deliver(self):
        for record in self:
            record.state = 'delivered'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
            
    def action_reset_to_draft(self):
        for record in self:
            record.state = 'new'

    @api.depends("order_lines.margin")
    def _compute_total_margin(self):
        for record in self:
            record.total_margin = sum(record.order_lines.mapped('margin'))

    def action_confirm(self):
        for record in self:
            for line in record.order_lines:
                stock_record = self.env['capy.stock'].search([('product_id', '=', line.product_id.id)], limit=1)
                if stock_record:
                    if stock_record.quantity < line.quantity:
                        raise UserError(f"Not enough capybaras in stock for {line.product_id.name}!")
                    stock_record.quantity -= line.quantity
            record.state = 'confirmed'