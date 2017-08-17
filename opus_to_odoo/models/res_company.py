# -*- coding: utf-8 -*-
# © <2017> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    server = fields.Char(
        required=True, string="Server")
    username = fields.Char(
        string='UserNamer', required=True,
    )
    password = fields.Char(
        string='Password', required=True,
    )
