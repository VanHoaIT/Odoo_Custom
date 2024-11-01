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
            'sale_order_checkout/static/src/views/*.xml',
            'sale_order_checkout/static/src/views/*.js',

            'sale_order_checkout/static/src/bundle/component/total_sales/*',
            'sale_order_checkout/static/src/bundle/component/revenue/*',
            'sale_order_checkout/static/src/bundle/component/average_order_value/*',
            'sale_order_checkout/static/src/bundle/component/total_orders/*',
            'sale_order_checkout/static/src/bundle/dashboard_action/*',
        ],
        'web.assets_fontend': [
       
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
