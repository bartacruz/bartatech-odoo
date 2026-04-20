import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useFullCalendar } from "@web/views/calendar/hooks";
import { useService } from "@web/core/utils/hooks";

export class M2MCalendarWidget extends Component {
  static template = "appointments.M2MCalendarWidget";
  static props = { ...standardFieldProps };
  setup() {
    // This.calendarRef = useRef("calendar-container");
    this.orm = useService("orm");
    this.fc = useFullCalendar("calendar-container", this.options);
  }
  get options() {
    return {
      allDaySlot: true,
      allDayContent: "",
      events: (_, successCb) => successCb(this.fetchEvents()),
      slotLabelFormat: {
        hour: "numeric",
        minute: "2-digit",
        hour12: false,
        omitZeroMinute: false,
      },
      eventClick: this.onEventClick,
      eventDisplay: "block",
      selectMinDistance: 5,
      initialView: "dayGridMonth",
    };
  }
  onEventClick(ev) {
    const slot = this.props.record.data[this.props.name].records[ev.event.id];
    console.debug("slot", slot);
  }
  fetchEvents(props = this.props) {
    const slots = props.record.data[props.name].records;
    const slots_map = slots.map((r) => ({
      id: r.data.id,
      title: "disponible",
      start: r.data.date_from.toISO(),
      end: r.data.date_to.toISO(),
      allDay: false,
    }));

    return slots_map;
  }
  mapRecordsToEvents() {
    return Object.values(this.props.record.data[this.props.name].records).map(
      (r) => this.convertRecordToEvent(r),
    );
  }
  convertRecordToEvent(record) {
    return {
      id: record.id,
      title: record.date_from,
      start: record.date_from.toISO(),
      end: record.date_to.toISO(),
      allDay: false,
    };
  }

  async updateEvents(nextProps) {
    if (this.calendar) {
      const newEvents = await this.fetchEvents(nextProps);
      this.calendar.removeAllEvents();
      this.calendar.addEventSource(newEvents);
    }
  }
}

registry.category("fields").add("m2m_calendar", {
  component: M2MCalendarWidget,
  supportedTypes: ["many2many"],
  relatedFields: () => {
    return [
      { name: "id", type: "int" },
      { name: "display_name", type: "char" },
      { name: "date_from", type: "date" },
      { name: "date_to", type: "date" },
    ];
  },
});
