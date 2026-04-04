from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _desc = "Estate Property Types"

    name = fields.Char(required = True)
    _unique_type_name = models.Constraint('UNIQUE(name)', 'Porperty Type must be unique')