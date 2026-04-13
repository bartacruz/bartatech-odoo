from odoo import _, api, fields, models
from odoo.tools.translate import html_translate


class PMProperty(models.Model):
    _name = 'pm.property'
    _description = 'Property'
    _inherits = {"res.partner": "partner_id"}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    partner_id = fields.Many2one(
        string="Property",
        help="Current property",
        comodel_name="res.partner",
        required=True,
        index=True,
        ondelete="restrict",
    )
    description = fields.Html(string='Description', translate=html_translate, sanitize_attributes=False, sanitize_form=False)
    state = fields.Selection([
        ('available','Available'),
        ('rented','Rented'),
        ('not available','Not Available'),
        ],
        default='available'
    )
    
    property_type_id = fields.Many2one('pm.property.type')
    rent_ids = fields.One2many('pm.rent','property_id')
    rent_count = fields.Integer(compute='_compute_rent_count')
    tenant_id = fields.Many2one('res.partner', compute="_compute_tenant",store=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=lambda self: self.env.company.country_id)
    checkout_time = fields.Float()
    
    @api.model
    def default_get(self, fields_list):
        res = super(PMProperty, self).default_get(fields_list)
        if 'checkout_time' in fields_list:
            default_val = self.env['ir.config_parameter'].sudo().get_param('property_management.pm_checkout_time', 10.0)
            res.update({'checkout_time': float(default_val)})
            
        return res
    @api.depends('rent_ids')
    def _compute_rent_count(self):
        for record in self:
            record.rent_count = len(record.rent_ids)
    
    @api.depends('rent_ids.state')
    def _compute_tenant(self):
        for record in self:
            record.tenant_id = record.rent_ids.filtered(lambda rent: rent.state == 'active').tenant_id
            if record.tenant_id and record.state == 'available':
                record.state = 'rented'
            if not record.tenant_id and record.state == 'rented':
                record.state = 'available'
            
    
    def show_rents(self):
        action = self.env.ref("property_management.action_pm_rent").read()[0]
        action["context"] = {'default_property_id':self.id}
        action["domain"] = [("id", "in", self.rent_ids.ids)]
        return action

    def action_rent(self):
        action = self.env.ref("property_management.action_pm_rent").read()[0]
        action["context"] = {'default_property_id':self.id, 'default_state':'reserved'}
        action['views'] = [(False, 'form')]
        action['view_mode'] = 'form'
        action['res_id'] = False
        action['target'] = 'new'
        return action
        
