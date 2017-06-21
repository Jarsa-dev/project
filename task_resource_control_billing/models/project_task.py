# -*- coding: utf-8 -*-
# <2016> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.multi
    @api.depends('line_billing_ids', 'real_qty')
    def _compute_remaining_quantity(self):
        super(ProjectTask, self)._compute_remaining_quantity()
        for rec in self:
            billing_request_total = 0.0
            for line in rec.line_billing_ids:
                billing_request_total += line.quantity
            rec.remaining_quantity = rec.real_qty - billing_request_total
