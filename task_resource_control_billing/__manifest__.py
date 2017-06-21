# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Resource Control Billing',
    'summary': 'Resource control Billing',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules',
    'author': (
        'Jarsa sistemas S.A de C.V. ,'
        'Odoo Community Association (OCA)'),
    'website': 'https://www.odoo-community.org',
    'license': 'LGPL-3',
    'depends': [
        'task_resource_control',
        'analytic_billing_plan',
        ],

    'data': [
        'wizards/resource_control.xml',
        'wizards/billing_request_view.xml',
    ],
    'installable': True,
}
