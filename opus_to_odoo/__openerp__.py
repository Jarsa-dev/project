# -*- coding: utf-8 -*-
# © 2017 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Opus to Odoo",
    "summary": "Import project of Opus to Odoo",
    "version": "9.0.1.0.0",
    "category": "Hidden",
    "website": "https://www.jarsa.com.mx/",
    "author": "JARSA Sistemas, S.A. de C.V.",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        'project'
    ],
    "data": [
        'wizards/import_opus_wizard_view.xml',
        'views/res_config_view.xml',
    ],
    "demo": [
    ]
}
