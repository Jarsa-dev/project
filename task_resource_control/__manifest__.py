# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Resource control',
    'summary': 'Resource control',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Jarsa sistemas S.A de C.V. ,'
        'Odoo Community Association (OCA)'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'product',
        'project_wbs_element',
        'purchase_request_to_rfq',
        'task_resource',
        ],

    'data': [
        'security/ir.model.access.csv',
        'wizards/resource_control.xml',
        'views/project_project_view.xml',
        'views/project_wbs_element.xml',
        'views/resource_control_view.xml',
        'views/task_resource.xml',
        'views/total_task_resource_view.xml',
    ],
    'installable': True,
}
