from odoo import models, fields, api

class CapyInvoice(models.Model):
    _name = "capy.invoice"
    _description = "The bill/invoice for the purchase of Capybara plushies"

    name = fields.Char(required = True)
    order_id = fields.Many2one("capy.order", required = True)
    customer_id = fields.Many2one("capy.customer", required = True)
    payment_ids = fields.One2many("capy.payment", "invoice_id")
    invoice_date = fields.Date(default = fields.Date.today)
    due_date = fields.Date()
    amount_paid = fields.Float(compute = "_compute_amount_paid", default = 0.0)
    amount_due = fields.Float(compute = "_compute_pending_amount")
    state = fields.Selection(selection = [('draft', "Draft"), ('pending', "Pending"), ('paid', "Paid"), ('cancelled', "Cancelled"), ('overdue', "Overdue")], default = 'draft') 

    @api.depends("order_id.total_amount")
    def _compute_pending_amount(self):
        for record in self:
            record.amount_due = record.order_id.total_amount - record.amount_paid
        if record.amount_due <=0 and record.state != 'cancelled':
            record.state = 'paid'

    @api.depends("payment_ids.amount")
    def _compute_amount_paid(self):
        for record in self:
            record.amount_paid = sum(record.payment_ids.mapped('amount'))

    @api.depends("payment_ids.amount", "order_id.total_amount")
    def _compute_state(self):
        for record in self:
            if record.amount_due <= 0:
                record.state = 'paid'
            else:
                record.state = 'pending'