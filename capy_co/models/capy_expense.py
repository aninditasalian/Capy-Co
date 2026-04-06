from odoo import models, fields

class CapyExpense(models.Model):
    _name = "capy.expense"
    _description = "List of Business expenses made by employees"

    name = fields.Char(required = True)
    employee_id = fields.Many2one("capy.employee", required = True)
    amount = fields.Float(default = 0.0, required = True)
    expense_date = fields.Date(default = fields.Date.today)
    category = fields.Selection(selection = [('travel', "Travel"), ('equipment', "Equipment"), ('marketing', "Marketing"), ('supplies', "Supplies"), ('other', "Other")], default = 'other')
    state = fields.Selection(selection = [('draft', "Draft"), ('submitted', "Submitted"), ('approved', "Approved"), ('rejected', "Rejected"), ('paid', "Paid")], default = 'draft')
    description = fields.Text()

    def action_submit(self):
        for record in self:
            record.state = 'submitted'

    def action_approve(self):
        for record in self:
            record.state = 'approved'

    def action_reject(self):
        for record in self:
            record.state = 'rejected'