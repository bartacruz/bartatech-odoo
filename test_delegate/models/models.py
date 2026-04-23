from odoo import models, fields, api


class Meter(models.Model):
    _inherit = "meter"

    fsm_equipment_id = fields.Many2one(
        "fsm.equipment",
        string="Related FSM Equipment",
        required=True,
        ondelete="restrict",
        delegate=True,
        auto_join=True,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        FSMEquipement = self.env["fsm.equipment"]
        for vals in vals_list:
            fsm_equipment_id = FSMEquipement.create(
                {
                    "name": vals.get("name", False),
                    "is_metered": True,
                }
            )
            if fsm_equipment_id:
                vals.update({"fsm_equipment_id": fsm_equipment_id.id})
        return super().create(vals_list)


class FSMEquipment(models.Model):
    _inherit = "fsm.equipment"

    is_metered = fields.Boolean()


# class test_delegate(models.Model):
#     _name = 'test_delegate.test_delegate'
#     _description = 'test_delegate.test_delegate'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
