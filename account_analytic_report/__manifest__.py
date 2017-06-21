# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Analytic Report",
    "version": "10.0.1.0.0",
    "depends": [
        'account', 'analytic'
    ],
    "author": "Odoo Community Association (OCA), JARSA Sistemas, S.A. de C.V.",
    "license": "AGPL-3",
    "category": "Accounting",
    "demo": [],
    "test": [],
    "data": [
        'view/analytic_view.xml',
        'wizards/account_analytic_chart_view.xml',
    ],
    'application': False,
    "installable": True,
}
