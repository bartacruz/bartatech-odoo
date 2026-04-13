from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pm_checkout_time = fields.Float(
        string="Default Check-out time",
        config_parameter='property_management.pm_checkout_time',
        default=10.0
    )