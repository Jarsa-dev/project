# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Analytic Plan',
    'version': '9.0.1.0.0',
    'author': (
        'Jarsa Sistemas, S.A de C.V.,'
        'Odoo Community Association (OCA)'),
    'description': 'This module is to analytic plan',
    'website': 'https://www.jarsa.com.mx',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'depends': [
        'project_wbs_element',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/analytic_plan_view.xml',
        'views/analytic_plan_version_view.xml',
        'views/analytic_plan_journal_view.xml',
        'views/project_view.xml',
    ],
    'installable': True,
    'active': False,
}
