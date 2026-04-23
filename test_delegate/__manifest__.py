{
    "name": "test_delegate",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "author": "My Company",
    "website": "https://github.com/bartacruz/bartatech-odoo",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "version": "18.0.0.1.0",
    "depends": ["meter", "fieldservice"],
    "pre_init_hook": "pre_init_hook",
    #'post_init_hook': 'post_init_hook',
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
    ],
}
