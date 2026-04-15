{
    "name": "Appointments",
    "summary": "Utilities for managing appointments and time slots",
    "author": "Julio Santa Cruz",
    "website": "https://github.com/bartacruz/bartatech-odoo",
    "category": "Uncategorized",
    "version": "18.0.0.0.1",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "development_status": "Alpha",
    "depends": ["base", "web", "calendar"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/appointment.xml",
        "views/res_partner.xml",
        "views/time_shift.xml",
        "wizards/appointment_wizard.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "appointments/static/src/js/m2mcalendar.css",
            "appointments/static/src/js/m2mcalendar.js",
            "appointments/static/src/js/m2mcalendar.xml",
        ],
    },
}
