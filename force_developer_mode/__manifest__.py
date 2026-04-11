# -*- coding: utf-8 -*-
{
    'name': "Force Developer Mode",

    'summary': "Force developer mode if you are an admin",

    'description': """
Force developer mode if you are an admin
    """,

    'author': "Bartatech",
    'website': "https://github.com/bartacruz/bartatech-odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Ucategorized',
    'version': '18.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    'assets': {
        'web.assets_backend': [
            'force_developer_mode/static/src/js/force_developer_mode.js'
        ]
    }
        
}

