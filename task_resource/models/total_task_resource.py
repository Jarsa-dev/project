# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class TotalTaskResource(models.Model):
    _name = "total.task.resource"

    resource_line_ids = fields.One2many(
        'analytic.resource.plan.line',
        'task_resource_id')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    subtotal = fields.Float(compute='_compute_value_subtotal')
    unit_price = fields.Float()
    qty_total = fields.Float()

    @api.multi
    @api.depends('qty', 'unit_price')
    def _compute_value_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price
