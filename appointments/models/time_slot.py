from odoo import models, fields


class TimeSlot(models.TransientModel):
    _name = "time.slot"
    _description = "defines a time slot"

    owner_id = fields.Many2one("res.partner")
    date_from = fields.Datetime()
    date_to = fields.Datetime()


class TimeSlotMixin(models.AbstractModel):
    _name = "time.slot.mixin"
    _description = "Mixin for classes that fit in time slots"

    date_from = fields.Datetime()
    date_to = fields.Datetime()
    duration = fields.Float(compute="_compute_duration", readonly=True)

    def _compute_duration(self):
        for record in self:
            if record.date_from and record.date_to:
                delta = record.date_to - record.date_from
                record.duration = delta.total_seconds() / 3600.0
            else:
                record.duration = 0.0
