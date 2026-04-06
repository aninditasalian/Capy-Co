from odoo import models, fields

class CapyApproval(models.Model):
    _name = "capy.approval"
    _description = "List of internal requestions which require the approval of a manager level employee"

    name = fields.Char(required = True)
    employee_id = fields.Many2one("capy.employee", required = True)
    manager_id = fields.Many2one("capy.employee", required = True)
    approval_type = fields.Selection(selection = [('discount', "Discount"), ('refund', "Refund"), ('expense', "Expense"), ('purchase', "Purchase"), ('other', "Other")], default = 'other')
    state = fields.Selection(selection = [('draft', "Draft"), ('pending', "Pending"), ('approved', "Approved"), ('rejected', "Rejected")], default = 'draft')
    reason = fields.Text()
    request_date = fields.Date(default = fields.Date.today)
    response_date = fields.Date()

    def action_submit(self):
        for record in self:
            record.state = 'pending'

    def action_approve(self):
        for record in self:
            record.state = 'approved'
            record.response_date = fields.Date.today()

    def action_reject(self):
        for record in self:
            record.state = 'rejected'
            record.response_date = fields.Date.today()

