# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Task Resource',
    'summary': 'Task Resource',
    'version': '11.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Eficent Business and IT Consulting Services S.L.,'
        'Odoo Community Association (OCA), Jarsa Sistemas S.A. de C.V.'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'product',
        'project_wbs_element',
        'purchase',
    ],

    'data': [
        'data/resource_type_data.xml',
        'security/ir.model.access.csv',
        'wizards/project_task_confirm_wizard_view.xml',
        'wizards/purchase_request.xml',
        # 'wizards/purchase_request_line_make_purchase_order_view.xml',
        'views/task_resource_view.xml',
        'views/project_wbs_element_view.xml',
        'views/project_project_view.xml',
        'views/purchase_order_view.xml',
        # 'views/purchase_request_view.xml',
        'views/resource_type_view.xml',
        'views/total_task_resource_view.xml',
    ],
    'installable': True,
}
