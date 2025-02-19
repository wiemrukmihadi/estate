from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _inherit = "estate.mixin"
    _description = 'Estate Property Tag'
    _order = "name desc"

    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique')]
    color = fields.Integer()