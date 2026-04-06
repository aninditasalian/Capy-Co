from odoo import models, fields

class CapyExpense(models.Model):
    _name = "capy.expense"
    _description = "List of Business expenses made by employees"

    name = fields.Char(required = True)
    employee_id = fields.Many2one("capy.employee", required = True)
    approval_id= fields.Many2one("capy.approval", string = "Approval")
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

    def write(self, vals):
        rec = super().write(vals)
        if vals.get('state') == 'submitted':
            for record in self:
                approval = self.env['capy.approval'].create({
                    'name': "EXP-APPR" + record.name,
                    'employee_id': record.employee_id.id,
                    'approval_type': 'expense',
                    'state': 'pending',
                    'reason': record.description,
                    'request_date': fields.Date.today(),
                    })
                record.approval_id = approval
        return rec