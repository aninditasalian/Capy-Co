from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CapySupplier(models.Model):
    _name = "capy.supplier"
    _description = "List of the manufacturers and wholesalers of the CapyCo Plushies."

    name = fields.Char(required = True) #Company Name
    contact_name = fields.Char(required = True) #Contact within the company
    email = fields.Char(required = True)
    phone = fields.Char(required = True) #Country code used '+' therefore datatype is CHAR and not Integer
    address = fields.Text(required = True)
    country = fields.Char(required = True)
    deliv_time = fields.Integer(default = 7)
    main_supplier = fields.Boolean(string="Main Supplier", default = False)
    total_supplied = fields.Integer(compute = '_compute_total_supplied')
    notes = fields.Text()

    @api.depends()
    def _compute_total_supplied(self):
        for record in self:
            record.total_supplied = self.env['capy.purchase.order'].search_count([('supplier_id', '=', record.id)])

    @api.constrains('main_supplier')
    def _check_unique_main_supplier(self):
        for record in self:
            if record.main_supplier: #searches for any other supplier marked as main
                other_main = self.search([
                    ('main_supplier', '=', True),
                    ('id', '!=', record.id)
                ])
                if other_main:
                    raise ValidationError(
                        f"Only one supplier can be the Main Supplier. "
                        f"'{other_main[0].name}' is already set as main."
                    )