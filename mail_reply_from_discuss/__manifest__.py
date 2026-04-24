{
    "name": "Mail: Reply from discuss",
    "summary": "Reply to incomming mails from discuss",
    "author": "Julio Santa Cruz",
    "website": "https://github.com/bartacruz/bartatech-odoo",
    "category": "Discuss",
    "version": "18.0.0.0.1",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "development_status": "Alpha",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_message.xml",
    ],
    "assets": {
        "web.assets_backend": ["mail_reply_from_discuss/static/src/components/**/*"],
    },
}
