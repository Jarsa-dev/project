# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Analytic Billing Plan',
    'version': '11.0.1.0.0',
    'author': (
        'Jarsa Sistemas, S.A de C.V., Odoo Community Association (OCA)'),
    'website': 'https://www.jarsa.com.mx',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'depends': [
        'project_task_resource',
        'project_wbs_element',
        'account',
    ],
    'data': [
        'data/product_product_data.xml',
        'data/data.xml',
        'wizard/billing_request_view.xml',
        'security/ir.model.access.csv',
        'views/account_invoice_line_view.xml',
        'views/analytic_billing_view.xml',
        'views/analytic_billing_plan_line_view.xml',
        'views/project_wbs_element.xml',
        'views/project_project_view.xml',
        # 'views/res_config_view.xml',
        'views/task_resource.xml',
    ],
    'installable': True,
}
