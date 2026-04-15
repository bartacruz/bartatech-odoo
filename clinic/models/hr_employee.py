from odoo import api, fields, models
from ast import literal_eval


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    booking_combination_id = fields.Many2one("resource.booking.combination")
    booking_type_id = fields.Many2one("resource.booking.type")

    def _generate_booking_combination(self):
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("clinic.booking_departments", False)
        )
        if not param:
            return
        booking_departments = literal_eval(param)
        for employee in self:
            if (
                not employee.department_id
                or employee.department_id.id not in booking_departments
            ):
                continue
            resource = employee.resource_id
            if not employee.booking_combination_id:
                employee.booking_combination_id = self.env[
                    "resource.booking.combination"
                ].create(
                    {"name": f"{employee.name}", "resource_ids": [(4, resource.id)]}
                )
            if not employee.booking_type_id:
                booking_type = self.env["resource.booking.type"].create(
                    {
                        "name": f"{employee.department_id.name} - {employee.name}",
                        "duration": 0.5,
                    }
                )

                self.env["resource.booking.type.combination.rel"].create(
                    {
                        "type_id": booking_type.id,
                        "combination_id": employee.booking_combination_id.id,
                    }
                )

                # 3. Guardamos el ID en el empleado
                employee.booking_type_id = booking_type

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)
        employees._generate_booking_combination()
        return employees
