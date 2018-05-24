# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project Picking Type',
    'summary': 'Picking Type OUT/IN',
    'version': '11.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Jarsa Sistemas S.A. de C.V., Odoo Community Association (OCA)'),
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'stock',
        'project_task_resource',
        ],
    'data': [
        'views/project_project_view.xml',
        'views/stock_picking_type_view.xml',
    ],
    'installable': True,
}
