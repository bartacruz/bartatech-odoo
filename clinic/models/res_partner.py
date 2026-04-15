from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    clinic_record_ids = fields.One2many("clinic.record", "patient_id")
    clinic_record_count = fields.Integer(compute="_compute_clinic_records")

    @api.depends("clinic_record_ids")
    def _compute_clinic_records(self):
        for record in self:
            record.clinic_record_count = len(record.clinic_record_ids)

    def action_open_clinic_records(self):
        action = self.env.ref("clinic.action_clinic_record").read()[0]
        action["context"] = {"default_patient_id": self.id}
        action["domain"] = [("id", "in", self.clinic_record_ids.ids)]
        return action
