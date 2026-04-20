from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import pytz


class PMRent(models.Model):
    _name = "pm.rent"
    _description = "Rent on a property"

    name = fields.Char(
        string="Rent Code",
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("reserved", "Reserved"),
            ("active", "Active"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ]
    )

    property_id = fields.Many2one("pm.property")
    tenant_id = fields.Many2one("res.partner")
    contact_phone = fields.Char(compute="_compute_contact_phone", store=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    duration = fields.Float(compute="_compute_duration", store="True")
    is_all_day = fields.Boolean(default=True)
    date_checkout = fields.Datetime(string="Check out")

    @api.constrains("date_start", "date_end")
    def _check_dates_order(self):
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_end < record.date_start
            ):
                raise ValidationError(
                    _("La fecha de fin no puede ser anterior a la fecha de inicio.")
                )

    @api.depends("tenant_id.phone", "tenant_id.mobile")
    def _compute_contact_phone(self):
        for rent in self:
            if not rent.contact_phone:
                rent.contact_phone = (
                    rent.tenant_id.phone or rent.tenant_id.mobile or False
                )

    @api.depends("date_start", "date_end")
    def _compute_duration(self):
        for record in self:
            if not record.date_start or not record.date_end:
                record.duration = 0
            else:
                record.duration = (record.date_end - record.date_start).days

    @api.depends("name", "tenant_id.name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} - {record.tenant_id.name}"

    @api.onchange("date_end", "property_id")
    def _onchange_dates_for_checkout(self):
        if self.date_end:
            h_float = self.property_id.checkout_time or float(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_management.pm_checkout_time", 10.0)
            )
            checkout_day = self.date_end + timedelta(days=1)
            hours = int(h_float)
            minutes = int((h_float - hours) * 60)
            naive_dt = datetime.combine(checkout_day, datetime.min.time()).replace(
                hour=hours, minute=minutes
            )
            tz = pytz.timezone(
                self.property_id.partner_id.tz or self.env.user.tz or "UTC"
            )
            local_dt = tz.localize(naive_dt, is_dst=None)
            self.date_checkout = local_dt.astimezone(pytz.utc).replace(tzinfo=None)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("pm.rent")
        return super().create(vals_list)

    def action_active(self):
        self.ensure_one()
        now = fields.Datetime.now()
        if not (self.date_start <= now <= self.date_end):
            raise ValidationError(
                _(
                    "No puedes activar el alquiler fuera del rango de fechas permitido.\n"
                    "Fecha actual: %{now}s\n"
                    "Rango: %{start}s a %{end}s"
                )
                % {
                    "now": fields.Datetime.context_timestamp(self, now).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "start": fields.Datetime.context_timestamp(
                        self, self.date_start
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "end": fields.Datetime.context_timestamp(
                        self, self.date_end
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        active_rents = self.property_id.rent_ids.filtered(
            lambda r: r.state == "active" and r.id != self.id
        )

        if active_rents:
            # Tomamos el nombre del primero que encontre para el error
            other_rent_name = active_rents[0].name
            raise ValidationError(
                _(
                    "La propiedad '%{prop}s' ya tiene un alquiler activo (Código: %{code}s). "
                    "Finalizá el anterior antes de activar este."
                )
                % {"prop": self.property_id.name, "code": other_rent_name}
            )

        self.state = "active"
