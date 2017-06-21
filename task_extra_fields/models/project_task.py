# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    direct_cost = fields.Float(
        compute='_compute_direct_cost',
        string='Direct Cost')
    indirects = fields.Float(
        default="1.0",
        string="Indirects Percentage",
        help="Percentage of Indirects",)
    indirects_amount = fields.Float(
        compute='_compute_indirects_value',
        string='Indirects Amount')
    field_indirects = fields.Float(
        default="1.0",
        string="Field Indirects Percentage",
        help="Percentage of Field Indirects",)
    field_indirects_amount = fields.Float(
        compute='_compute_field_indirects_value',
        string='Field Indirects Amount')
    percentages_subtotal = fields.Float(
        compute='_compute_percentages_subtotal',
        string="Percentages Subtotal",
        help="Subtotal compute by the summatory of the direct cost, indirects"
        " amount and field indirects amount")
    unit_price = fields.Float(compute='_compute_unit_price')
    subtotal = fields.Float(compute='_compute_value_subtotal')

    @api.multi
    @api.depends('resource_line_ids')
    def _compute_direct_cost(self):
        for rec in self:
            if rec.resource_line_ids:
                for line in rec.resource_line_ids:
                    rec.direct_cost += line.subtotal
            else:
                rec.direct_cost = 0.0

    @api.multi
    @api.depends('indirects')
    def _compute_indirects_value(self):
        for rec in self:
            rec.indirects_amount = rec.direct_cost * (rec.indirects / 100)

    @api.multi
    @api.depends('field_indirects')
    def _compute_field_indirects_value(self):
        for rec in self:
            rec.field_indirects_amount = rec.direct_cost * (
                rec.field_indirects / 100)

    @api.multi
    @api.depends('direct_cost', 'indirects_amount', 'field_indirects_amount')
    def _compute_percentages_subtotal(self):
        for rec in self:
            rec.percentages_subtotal = (
                rec.direct_cost + rec.indirects_amount +
                rec.field_indirects_amount)

    @api.multi
    @api.depends('percentages_subtotal')
    def _compute_unit_price(self):
        for rec in self:
            rec.unit_price = rec.percentages_subtotal

    @api.model
    def _compute_value_subtotal(self):
        for rec in self:
            rec.subtotal = rec.unit_price * rec.qty
