from odoo import models, fields

class CapyLead(models.Model):
    _name = "capy.lead"
    _description = "List of Possible Business ventures"

    name = fields.Char(required = True)
    customer_id = fields.Many2one("capy.customer", required = True) #Potential Customers 
    employee_id = fields.Many2one("capy.employee", required = True) #Salesperson who can handle this 
    expected_revenue = fields.Float(default = 0.0)
    state = fields.Selection(selection = [('new', "New"), ('contacted', "Contacted"), ('negotiating', "Negotiating"), ('won', "Won"), ('lost', "Lost")], default = 'new')
    priority = fields.Selection(selection = [('low', "Low"), ('medium', "Medium"), ('high', "High")], default = 'medium')
    deadline = fields.Date()
    description = fields.Text()