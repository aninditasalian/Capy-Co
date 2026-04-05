from odoo import models, fields, api

class CapyApproval(models.Model):
    _name = "capy.approval"
    _description = "List of internal requestions which require the approval of a manager level employee"

    name = fields.Char(required = True)
    employee_id = fields.Many2one("capy.employee", required = True)
    manager_id = fields.Many2one("capy.employee", required = False)
    approval_type = fields.Selection(selection = [('discount', "Discount"), ('refund', "Refund"), ('expense', "Expense"), ('purchase', "Purchase"), ('other', "Other")], default = 'other')
    state = fields.Selection(selection = [('draft', "Draft"), ('pending', "Pending"), ('approved', "Approved"), ('rejected', "Rejected")], default = 'draft')
    reason = fields.Text()
    request_date = fields.Date(default = fields.Date.today)
    response_date = fields.Date(default = fields.Date.today)

    def write(self, vals):
        rec = super().write(vals)
        if vals.get('state') == 'approved':
            for record in self:
                expense = self.env['capy.expense'].search([('approval_id', '=', record.id)])

                if expense:
                    expense.write({'state': 'approved'})
        if vals.get('state') == 'rejected':
            for record in self:
                expense = self.env['capy.expense'].search([('approval_id', '=', record.id)])

                if expense:
                    expense.write({'state': 'rejected'})
        return rec
                
