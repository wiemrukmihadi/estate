from odoo import api, models, fields, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _rec_name = 'property_id'

    price = fields.Float()
    status = fields.Selection(
        [
            ('new', 'New'),
            ('onprogress', 'On Progress'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)
            # offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)
    @api.depends('date_deadline')        
    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days
            # property.validity = (property.date_deadline - fields.Date.today()).days
    
    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Already accepted by partner"))
        self.status = "accepted"
        self.property_id.state = 'accepted'
        self.property_id.selling_price = self.price

    def action_refuse(self):
        self.ensure_one()
        self.status = "refused"