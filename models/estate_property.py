from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    _sql_constraints = [('unique_property_name', 'UNIQUE(name)', 'Property name must be unique')]

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    tag_ids = fields.Many2many('estate.property.tag')
    description = fields.Text()
    postcode = fields.Char(string='Postal Code')

    def _default_date(self):
        return fields.Date.today()
    date_availability = fields.Date(string="Date Availability", default=_default_date)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price')) if property.offer_ids else 0

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.onchange('garden_area')
    def _onchange_garden_area(self):
        for estate in self:
            if estate.garden_area <= 0:
                estate.garden = False
                estate.garden_orientation = 'north'
            else:
                estate.garden = True

    @api.onchange('garden')
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0
                estate.garden_orientation = 'north'
    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for estate in self:
            if estate.date_availability:
                if estate.date_availability < fields.Date.today():
                    # raise ValidationError(_("Date availability set in the past"))
                    return{
                        "warning": {
                            "title": _("Warning"),
                            "message": _('Date availability set in the past')
                        }
                    }
                    
            # return{
            #     "warning": {
            #         "title": _("Warning"),
            #         "message": _('My Message')
            #     }
            # }
    @api.constrains("selling_price")
    def _check_price_constraints(self):
        for estate in self:
            if estate.selling_price < 10000000:
                raise ValidationError(_("Selling price can not be lower than 10.000.000,00"))

    def action_sold(self):
        if "sold" in self.state:
            raise UserError(_("Already accepted by partner"))
        self.state = "sold"

    def action_cancel(self):
        self.state = "canceled"

    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation", required=True)
    
