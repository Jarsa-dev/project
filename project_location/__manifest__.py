# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project Location',
    'summary': 'Location for each project',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Jarsa Sistemas S.A. de C.V., Odoo Community Association (OCA)'),
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'stock',
        'task_resource',
        'project_picking_type',
        ],
    'data': [
        'views/project_project_view.xml',
    ],
    'installable': True,
}
