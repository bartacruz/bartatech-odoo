from odoo import api, fields, models


class PMPropertyType(models.Model):
    _name = "pm.property.type"
    _description = "Property type"

    name = fields.Char()
    description = fields.Char()
    property_ids = fields.One2many("pm.property", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")

    @api.depends("property_ids")
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)
