{
    'name': 'Hostel Management',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Manage hostel operations',
    'description': """Efficiently manage the entire residential facility in the school.""",
    'depends': ['base'],
    'data': [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "views/hostel.xml",
        "views/hostel_room.xml",
        "views/hostel_category.xml",
        "views/hostel_room_category.xml",
        "data/data.xml",
        'views/welcome_message.xml',

    ],
    'assets': {
        'web.assets_backend': [
            # 'my_hostel/static/static/src/js/welcome_message.js',
            # '/home/vanhoa/congviec/odoo/addons/purchase/static/src/views/purchase_dashboard.js',
        ],
    },

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

   
    # 'assets': {
    #     'web.assets_backend': [
    #         'web/static/src/xml/**/*',
    #     ],
    # },
    # 'demo': ['demo.xml'],