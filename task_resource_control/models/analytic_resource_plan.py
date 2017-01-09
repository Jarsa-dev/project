# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _inherit = "analytic.resource.plan.line"

    real_qty = fields.Float(string="Quantity Real")
    real_subtotal = fields.Float(
        string="Real Subtotal",
        compute='_compute_real_subtotal',)

    @api.depends('real_qty')
    def _compute_real_subtotal(self):
        for rec in self:
            rec.real_subtotal = rec.real_qty * rec.unit_price
