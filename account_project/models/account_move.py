# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        copy=False)
