{
    'name': 'Custom Sale Order',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Module to customize Sale Order',
    'description': """
        This module adds a Check-out Date field to the Sale Order.
    """,
    'depends': ['sale'],
    'data': [
        'views/sale_order_checkout_view.xml',
        'views/sale_menus.xml',        
    ],
    'assets':{
        'web.assets_backend': [
            'sale_order_checkout/static/src/views/sale_dashboard.xml',
            'sale_order_checkout/static/src/views/sale_dashboard.js',            
            'sale_order_checkout/static/src/views/sale_listview.xml',
            'sale_order_checkout/static/src/views/sale_listview.js',

            'sale_order_checkout/static/src/bundle/dashboard_action/dashboard_action.xml',
            'sale_order_checkout/static/src/bundle/dashboard_action/dashboard_action.scss',
            'sale_order_checkout/static/src/bundle/dashboard_action/dashboard_action.js',
        ],
        'web.assets_fontend': [
       
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
