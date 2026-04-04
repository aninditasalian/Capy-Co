from odoo import api, models, fields 

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _desc = "Estate Porperty Tags"

    name = fields.Char(required = True)
    _unique_tag_name = models.Constraint("UNIQUE(name)", "The name of the tag must be unique")