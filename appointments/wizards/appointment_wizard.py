from odoo import api,models,fields
from datetime import datetime, timedelta

class ApppointmentWizard(models.TransientModel):
    _name = 'appointment.wizard'
    _description = 'Appointment Wizard'
    
    provider_id = fields.Many2one('res.partner')
    time_shift_ids = fields.Many2many('time.shift', related='provider_id.time_shift_ids')
    date_start = fields.Date(default=fields.Date.today)
    date_end = fields.Date(compute="_compute_date_end", store=True)
    # Relación con los slots generados (para la vista calendario)
    slot_ids = fields.Many2many('time.slot', string="Slots Generados", compute="_compute_slots")
    
    @api.depends('date_start')
    def _compute_date_end(self):
        """Calcula la fecha de fin sumando 14 días a la fecha de inicio"""
        for record in self:
            record.date_end = record.date_start + timedelta(days=14)
            
    @api.depends('time_shift_ids','date_start','date_end')
    def _compute_slots(self):
        """Genera slots temporales cada vez que cambian los turnos seleccionados"""
        if not self.time_shift_ids:
            self.slot_ids = [(5, 0, 0)] # Limpiar
            print("slot_ids",self.slot_ids)
            return
        
        print(self.provider_id, self.time_shift_ids,"start",self.date_start,"end",self.date_end)
        for shift in self.time_shift_ids:
            # Reutilizamos tu lógica de diccionarios
            slots = shift.get_slots_in_range(self.date_start, self.date_end)
            print(shift,"slots:",slots)
            slots.owner_id = self.provider_id.id
            self.slot_ids |= slots
            