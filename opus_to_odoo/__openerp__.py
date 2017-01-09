# -*- coding: utf-8 -*-
# <2017> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Opus To Odoo',
    'version': '9.0.1.0.0',
    'author': (
        'Jarsa Sistemas, S.A de C.V., Odoo Community Association (OCA)'),
    'website': 'https://www.jarsa.com.mx',
    'category': 'Generic Modules',
    'license': 'AGPL-3',
    'depends': [
        'task_resource_control_billing',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/import_data_view.xml',
        'wizards/download_issues_file_view.xml',
    ],
    'installable': True,
}
