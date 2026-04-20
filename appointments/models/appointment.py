from odoo import models, fields


class Appointment(models.Model):
    _name = "appointment"
    _description = "an appointment between a requester and a provider"
    _inherit = ["time.slot.mixin"]

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ]
    )

    requester_id = fields.Many2one("res.partner")
    provider_id = fields.Many2one("res.partner")
