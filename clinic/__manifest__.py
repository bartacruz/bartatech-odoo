{
    "name": "Clinic Management",
    "summary": "Clinic Management Tools",
    "author": "Julio Santa Cruz",
    "website": "https://github.com/bartacruz/bartatech-odoo",
    "category": "Industries/Medical",
    "version": "18.0.0.0.1",
    "license": "AGPL-3",
    "depends": ["hr", "resource_booking", "web"],
    "assets": {
        "web.assets_backend": [
            "clinic/static/src/js/calendar_model.esm.js",
        ],
    },
    "data": [
        "security/ir.model.access.csv",
        "views/clinic_records.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
    ],
}
