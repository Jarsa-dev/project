# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    resource_control_ids = fields.One2many(
        'resource.control',
        'task_id',
        string='Resource change history')
    real_qty = fields.Float(
        string='Real Quantity',
        readonly=True,
        )
    real_subtotal = fields.Float(
        string='Real Subtotal',
        compute='_compute_real_subtotal',)
    qty = fields.Float(string='Planned Quantity',)

    @api.model
    def create(self, vals):
        res = super(ProjectTask, self).create(vals)
        if (res.real_qty and res.real_subtotal) == 0:
            res.real_qty = res.qty
            res.real_subtotal = res.subtotal
        return res

    @api.depends('qty')
    @api.multi
    def _compute_real_subtotal(self):
        for rec in self:
            rec.real_subtotal = rec.unit_price * rec.real_qty

    @api.multi
    def _update_real_qty(self, new_qty):
        for rec in self:
            resource_list = {
                x.product_id.name: x.qty
                for x in rec.resource_ids}
            for resource in rec.resource_line_ids:
                resource.real_qty = (
                    new_qty * resource_list[resource.product_id.name])
