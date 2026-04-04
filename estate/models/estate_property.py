from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class EstateProperties(models.Model):
    _name = "estate.property"
    _desc = "Estate Properties"

    name = fields.Char(required = True)
    desc = fields.Text()
    selling_price = fields.Float()
    expected_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute = "_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string= "Property Type")
    buyer_id = fields.Many2one("res.partner", string = "Buyers")
    salesperson_id = fields.Many2one("res.users", string = "salesperson", deafult = lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_price = fields.Float(compute = "_compute_best_price", string = "Best Price")

    state = fields.Selection(selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('offer_rejected', 'Offer Rejected'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default = 'new')
    _check_expected_price = models.Constraint('CHECK(expected_price > 0)', 'The expected price has to be positive')
    _check_selling_price = models.Constraint('CHECK(selling_price > 0)', 'The Selling price has to be positive')
    tag_ids = fields.Many2many("estate.property.tag")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    # @api.onchange("has_garden")
    # def _has_garden_(self):
    #     if not self.has_garden:
    #         self.garden_area = 0
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0
    
    def sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled Properties cannot be sold")
            else:
                record.state = "sold"
    
    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold Properties cannot be cancelled")
            else:
                record.state = "cancelled"

    @api.constrains('expected_price', 'selling_price')
    def _check_valid_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits = 2) < 0 and not float_is_zero(record.selling_price, precision_digits = 2):
                raise ValidationError('The selling price must not be less than 90 percent of the expected price!')