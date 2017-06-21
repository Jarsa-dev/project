# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Confirmed Sequence',
    'version': '10.0.1.0.0',
    'author': 'Jarsa Sistemas S.A. de C.V.,Odoo Community Association (OCA)',
    'description': (
        'This module adds a new sequence when the'
        'purchase order is confirmed'),
    'website': 'https://www.jarsa.com.mx',
    'category': 'Purchase',
    'depends': [
        'purchase'
    ],
    'data': [
        'data/data.xml'
    ],
    'installable': True,
    'active': True,
}
