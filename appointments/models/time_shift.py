from odoo import models, fields
from datetime import datetime, timedelta


class TimeShift(models.Model):
    _name = "time.shift"
    _description = "defines a time shift"

    name = fields.Char()
    day = fields.Selection(
        [
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday"),
            ("6", "Sunday"),
        ],
        required=True,
    )
    time_from = fields.Float("From")
    time_to = fields.Float("To")
    slot_duration = fields.Float()

    def _get_slots(self, day):
        self.ensure_one()
        slots = []
        target_date = fields.Date.to_date(day)
        if target_date.weekday() != int(self.day):
            return slots
        base_datetime = datetime.combine(target_date, datetime.min.time())
        current_time = self.time_from
        while current_time + self.slot_duration <= self.time_to + 1e-7:
            start_delta = timedelta(hours=current_time)
            end_delta = timedelta(hours=current_time + self.slot_duration)
            slots.append(
                {
                    "date_from": base_datetime + start_delta,
                    "date_to": base_datetime + end_delta,
                }
            )
            current_time += self.slot_duration
        return slots

    def _get_slots_in_range(self, date_start, date_end):
        self.ensure_one()
        all_slots = []

        curr_date = fields.Date.to_date(date_start)
        last_date = fields.Date.to_date(date_end)

        while curr_date <= last_date:
            all_slots.extend(self._get_slots(curr_date))
            curr_date += timedelta(days=1)

        return all_slots

    def get_slots_in_range(self, date_start, date_end):
        vals_list = self._get_slots_in_range(date_start, date_end)
        return self.env["time.slot"].create(vals_list)
