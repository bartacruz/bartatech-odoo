# -*- coding: utf-8 -*-
{
    'name': "Property Management",

    'summary': "Property Management System",

    'description': """
Property Management System
    """,

    'author': "Bartatech",
    'website': "https://github.com/bartacruz/bartatech-odoo",
    "license": "AGPL-3",
    'category': 'Uncategorized',
    'version': '18.0.0.0.4',
    'installable': True,
    'application': True,
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/pm_property.xml',
        'views/pm_property_types.xml',
        'views/pm_rent.xml',
        'views/res_config_settings.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

