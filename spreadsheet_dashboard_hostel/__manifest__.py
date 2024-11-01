# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Spreadsheet dashboard for hostel",
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Spreadsheet',
    'description': 'Spreadsheet',
    'depends': ['spreadsheet_dashboard', 'my_hostel'],
    'data': [
        "data/dashboards.xml",
    ],
    'auto_install': ['my_hostel'],
    'license': 'LGPL-3',
}
