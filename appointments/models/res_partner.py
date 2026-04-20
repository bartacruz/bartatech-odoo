from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    time_shift_ids = fields.Many2many("time.shift")
    appointment_ids = fields.One2many("appointment", "provider_id", readonly=True)
    appointment_count = fields.Integer(compute="_compute_appointment_count")

    def _compute_appointment_count(self):
        for partner in self:
            partner.appointment_count = len(partner.appointment_ids)

    def action_open_appointments(self):
        action = self.env.ref("appointments.appointment_wizard_action").read()[0]
        action["context"] = {"default_provider_id": self.id}
        return action
