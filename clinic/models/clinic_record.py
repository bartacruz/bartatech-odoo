from odoo import models, fields, api


class ClinicRecord(models.Model):
    _name = "clinic.record"
    _description = "A clinic record for a patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: "/",
        compute="_compute_name",
        store=True,
    )
    patient_id = fields.Many2one("res.partner")
    partner_id = fields.Many2one(
        "res.partner"
    )  # TODO: add a domain for doctors or employees

    summary = fields.Text()
    notes = fields.Text()

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("requested", "Requested"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
    )
    record_type = fields.Selection(
        [
            ("diagnostic", "Diagnostic"),
            ("lab", "Lab"),
            ("prescription", "Prescription"),
        ],
        required=True,
    )

    @api.depends("create_date")
    def _compute_name(self):
        for record in self:
            if record.name == "/":
                code = "clinic.record"
                record.name = self.env["ir.sequence"].next_by_code(code)
