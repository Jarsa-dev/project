# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Stock Project Consume',
    'summary': 'Stock Project Consume',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Jarsa Sistemas S.A. de C.V.',
        'Odoo Community Association (OCA)'),
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'account_accountant',
        'stock',
        'task_resource',
        ],

    'data': [
        'security/ir.model.access.csv',
        'views/analytic_resource_plan_view.xml',
        'wizards/resource_consume_view.xml'
    ],
    'installable': True,
}
