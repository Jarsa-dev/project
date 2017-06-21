# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    project_id = fields.Many2one(
        'project.project',
        string="Project",
        readonly=True)
