from odoo import fields, models, api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    clinic_booking_departments = fields.Many2many(
        comodel_name="hr.department",
        string="Booking Departments",
    )

    def set_values(self):
        ret = super().set_values()
        ids = self.clinic_booking_departments.ids
        self.env["ir.config_parameter"].sudo().set_param(
            "clinic.booking_departments", str(ids)
        )
        return ret

    @api.model
    def get_values(self):
        res = super().get_values()
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("clinic.booking_departments", "[]")
        )
        res.update(
            clinic_booking_departments=[(6, 0, literal_eval(param))],
        )
        return res
