from . import controllers
from . import models


def pre_init_hook(env):
    orphaned_meters = env["meter"].search([("fsm_equipment_id", "=", False)])
    orphaned_meters.action_unarchive()
    # print("pre_init", orphaned_meters, orphaned_meters.mapped("fsm_equipment_id"))


def post_init_hook(env):
    orphaned_meters = env["meter"].search([("fsm_equipment_id", "=", False)])
    for meter in orphaned_meters:
        equipment = env["fsm.equipment"].create(
            {"name": meter.name, "is_metered": True}
        )
        # print("post_init_hook: Created fsm_equipment ", equipment)
        meter.fsm_equipment_id = equipment.id
