# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class ProjectConfigSettings(models.Model):
    _inherit = 'project.config.settings'

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id,)
    server = fields.Char(
        related='company_id.server',)
    username = fields.Char(
        related='company_id.username',)
    password = fields.Char(
        related='company_id.password',)
