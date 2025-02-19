from odoo import _, api, models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _inherit = "estate.mixin"
    _description = 'Estate Property Type'
    _order = "sequence desc"

    _sql_constraints = [('unique_type_name', 'UNIQUE(name)', 'Property Type must be Unique')]

    sequence = fields.Integer(default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    property_count = fields.Integer(compute="_compute_property_count")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            self.env["estate.property.tag"].create(
                {
                    "name": vals.get("name"),
                }
            )
        return res
    def unlink(self):
        self.property_ids.state = "cancelled"
        return super().unlink()

    @api.depends("property_ids")
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    def action_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "estate.property",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id}
        }
