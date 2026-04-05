from odoo import models, fields

class CapyEmployee(models.Model):
    _name = "capy.employee"
    _description = "List of employees in CapyCo"

    name = fields.Char(required = True)
    email = fields.Char(required = True)
    phone = fields.Char(required = True)
    title = fields.Char(required = True)
    department = fields.Selection(selection = [('sales', "Sales"), ('finance', "Finance"), ('management', "Management"), ('warehouse', "Warehouse")], default = 'sales')
    hire_date = fields.Date(default = fields.Date.today)
    manager = fields.Boolean(default = False)
    status = fields.Selection(selection = [('intern', "Intern"), ('part_time', "Part-Time"), ('full_time', "Full Time"), ('fired', "Fired")], default = 'full_time')
    active = fields.Boolean(default = True)