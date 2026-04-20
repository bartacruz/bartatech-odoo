/** @odoo-module **/
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useFullCalendar } from "@web/views/calendar/hooks";
import { loadJS } from "@web/core/assets";

export class M2MCalendarWidget extends Component {
  static template = "appointments.M2MCalendarWidget";
  static props = { ...standardFieldProps };
  setup() {
    // this.calendarRef = useRef("calendar-container");
    this.orm = useService("orm");
    this.fc = useFullCalendar("calendar-container", this.options);
    onMounted(() => {
      console.debug("mounted");
      // console.debug("FULLC",this.fc);
      // // Verificamos si FullCalendar está disponible globalmente
      // if (window.FullCalendar) {
      //     this.renderCalendar();
      // } else {
      //     console.error("FullCalendar no está cargado en el sistema de Odoo.");
      // }
    });
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
    console.debug("eventClick", ev);
    const slot = this.props.record.data[this.props.name].records[ev.event.id];
    console.debug("slot", slot);
  }
  fetchEvents(props = this.props) {
    console.debug("FETCHEVENTS", props);
    console.debug("FETCHEVENTS data", props.record.data[props.name].records);
    const slots = props.record.data[props.name].records;
    const fafafa = slots.map((r) => ({
      id: r.data.id,
      title: "disponible",
      start: r.data.date_from.toISO(),
      end: r.data.date_to.toISO(),
      allDay: false,
    }));
    console.debug("FETCHEVENTS fafafa", fafafa);
    return fafafa;
    // const xids = props.record.data[props.name].resIds;
    // const ids = props.record.data[props.name]._currentIds;
    // console.debug("FETCHEVENTS ids",ids);
    // if (!ids.length) return [];

    // const records = await this.orm.read("time.slot", ids, ["display_name", "date_from", "date_to"]);
    // console.debug("FETCHEVENTS RECORDS",records);
    // return records.map(r => ({
    //     id: r.id,
    //     title: r.display_name,
    //     start: r.date_from,
    //     end: r.date_to,
    //     allDay: false
    // }));
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
  // async renderCalendar() {
  //     const events = await this.fetchEvents();
  //     // Odoo 18 suele usar la versión 5 o 6 de FullCalendar
  //     this.calendar = new window.FullCalendar.Calendar(this.calendarRef.el, {
  //         // En versiones nuevas, los plugins se cargan distinto o vienen integrados
  //         initialView: 'dayGridMonth',
  //         locale: 'es',
  //         events: events,
  //     });
  //     this.calendar.render();
  // }

  async updateEvents(nextProps) {
    console.debug("UPDATE EVENTS", nextProps);
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
  relatedFields: (fieldInfo) => {
    return [
      { name: "id", type: "int" },
      { name: "display_name", type: "char" },
      { name: "date_from", type: "date" },
      { name: "date_to", type: "date" },
    ];
  },
});
