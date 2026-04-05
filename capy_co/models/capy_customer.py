from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class CapyCustomer(models.Model):
    _name = "capy.customer"
    _description = "List of Customers of Capybara Plushies"

    name = fields.Char(required = True)
    email = fields.Char(required = True)
    phone = fields.Char(required = True) #Country code used '+' therefore datatype is CHAR and not Integer
    address = fields.Text(required = True)
    city = fields.Char(required = True)
    country = fields.Char(required = True)
    date_joined = fields.Date() #When the person be came a customer\
    VIP = fields.Boolean() #if the person is buying in bulk they are classified as VIP buyers
    total_orders = fields.Integer(compute = '_compute_total_orders')
    total_spent = fields.Float(compute = '_compute_total_spent')
    notes = fields.Text()

    @api.depends()
    def _compute_total_orders(self):
        for record in self:
            record.total_orders = self.env['capy.order'].search_count([('customer_id', '=', record.id)])

    @api.depends()
    def _compute_total_spent(self):
        for record in self:
            spent = self.env['capy.payment'].search([('customer_id', '=', record.id)])
            record.total_spent = sum(spent.mapped('amount'))

    @api.constrains('email')
    def _check_email_validity(self):
        for record in self:
            if record.email and "@" not in record.email:
                raise ValidationError("Invalid Email: The email address must contain an '@' symbol.")

