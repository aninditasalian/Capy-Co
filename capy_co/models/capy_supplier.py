from odoo import models, fields, api

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
    main_supplier = fields.Boolean(default = False)
    total_supplied = fields.Integer(compute = '_compute_total_supplied')

    @api.depends()
    def _compute_total_supplied(self):
        for record in self:
            record.total_supplied = self.env['capy.purchase.order'].search_count([('supplier_id', '=', record.id)])