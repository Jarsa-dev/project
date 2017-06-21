# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Task Resource',
    'summary': 'Task Resource',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Eficent Business and IT Consulting Services S.L.,'
        'Odoo Community Association (OCA)'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': [
        'project',
        'product',
        'project_wbs_element',
        'purchase_request_to_rfq',
        'purchase_confirmed_sequence',
    ],

    'data': [
        'data/resource_type_data.xml',
        'security/ir.model.access.csv',
        'wizards/project_task_confirm_wizard_view.xml',
        'wizards/purchase_request.xml',
        'wizards/purchase_request_line_make_purchase_order_view.xml',
        'views/total_task_resource_view.xml',
        'views/task_resource.xml',
        'views/project_wbs_element.xml',
        'views/project_project_view.xml',
        'views/purchase_order_view.xml',
        'views/purchase_request_view.xml',
        'views/resource_type_view.xml',
    ],
    'installable': True,
}
