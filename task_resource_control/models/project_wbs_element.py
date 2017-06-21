# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    total_real_charge = fields.Float(
        compute="_compute_total_real_charge",
        string='Total Real',)

    @api.multi
    def _compute_total_real_charge(self):
        for record in self:
            if not record.child_ids:
                for child in record.task_ids:
                    record.total_real_charge = (
                        record.total_real_charge + child.real_subtotal)
        for rec in self:
            if rec.child_ids:
                for child in rec.child_ids:
                    rec.total_real_charge = (
                        rec.total_real_charge + child.total_real_charge)
