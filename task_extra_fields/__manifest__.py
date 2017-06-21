# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Task Extra Fields',
    'summary': 'Add Fields to the task to compute extra percentages',
    'version': '10.0.1.0.0',
    'description': 'This module allows the compute of the task subtotal'
                   'with extra values for example: indirects percentages',
    'category': 'Generic Modules',
    'author': (
        'Jarsa Sistemas S.A. de C.V.'),
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'task_resource',
        ],

    'data': [
        'security/ir.model.access.csv',
        'views/project_task_view.xml',
    ],
    'installable': True,
}
