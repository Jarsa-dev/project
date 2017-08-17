# -*- coding: utf-8 -*-
# © <2017> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    opus_server = fields.Char(
        string="Opus Server",)
    opus_username = fields.Char(
        string="Opus Username",)
    opus_password = fields.Char(
        string="Opus Password",)
