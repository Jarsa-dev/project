# -*- coding: utf-8 -*-

from odoo import fields, models


class view(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('gantt8', 'Gantt8')])
