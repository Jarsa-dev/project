# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas S.A. de C.V.

from odoo import fields, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    date_start = fields.Date(
        string='Date Start',
        default=fields.Date.today,
        )
    date_end = fields.Date(
        string='Date End',
        default=fields.Date.today,
        )
