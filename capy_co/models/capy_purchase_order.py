from odoo import models, fields, api

class CapyPurchaseOrder(models.Model):
    _name = "capy.purchase.order"
    _description = "List of the purchase orders given by CapyCo to restock the Capybara plushies"

    name = fields.Char(string="Order ID", required=True, copy=False, readonly=True, default='Draft')
    supplier_id = fields.Many2one("capy.supplier", required = True)
    order_date = fields.Date(default = fields.Date.today)
    expected_date = fields.Date()
    state = fields.Selection(selection = [('draft', "Draft"), ('confirmed', "Confirmed"), ('received', "Received"), ('cancelled', "Cancelled")], default = 'draft')
    order_lines = fields.One2many("capy.purchase.order.line", "purchase_order_id")
    total_cost = fields.Float(string="Total Cost", compute = "_compute_total_cost", store=True, group_operator="sum")
    notes = fields.Text()

    @api.depends("order_lines.subtotal")
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(record.order_lines.mapped('subtotal'))

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
    
    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Draft') == 'Draft':
                order_date = vals.get('order_date') or fields.Date.today()
                vals['name'] = self.env['ir.sequence'].next_by_code('capy.purchase.order', sequence_date=order_date) or 'Draft'
        return super().create(vals_list)    

    def action_received(self): #updates stock after order is received
        for order in self:
            for line in order.order_lines: #finds the stock record for the product
                stock_record = self.env['capy.stock'].search([('product_id', '=', line.product_id.id)], limit=1)

                if stock_record:
                    stock_record.quantity += line.quantity
                    stock_record.last_updated = fields.Date.today()
                else: #create stock record if doesn't exist
                    self.env['capy.stock'].create({
                        'product_id': line.product_id.id,
                        'quantity': line.quantity,
                        'location': 'Warehouse',
                    })
            order.state = 'received'

    @api.onchange('supplier_id', 'order_date')
    def _onchange_expected_date(self):
        if self.supplier_id and self.order_date:
            days_to_add = self.supplier_id.deliv_time or 7 
            self.expected_date = fields.Date.add(self.order_date, days=days_to_add)