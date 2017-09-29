# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project WBS Element',
    'summary': 'Manage Work Breakdown Structures in your Projects',
    'version': '11.0.1.0.0',
    'author': (
        'Eficent Business and IT Consulting Services S.L.,'
        'Odoo Community Association (OCA), Jarsa Sistemas S.A. de C.V.'),
    'website': 'https://www.odoo-community.org',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'project_image',
    ],
    'data': [
        'views/project_task_view.xml',
        'views/project_wbs_element_view.xml',
        'views/project_view.xml',
    ],
    'installable': True,
}
