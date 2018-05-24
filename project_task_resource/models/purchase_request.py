# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',)
