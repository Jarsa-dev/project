# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _inherit = "analytic.resource.plan.line"

    qty = fields.Float(
        string="Quantity Planned",
        digits=(14, 5),)
    qty_on_hand = fields.Float(
        string="Quantity on Hand",
        digits=(14, 5),
        compute="_compute_qty_on_hand",
        )
    qty_consumed = fields.Float(
        string="Quantity Consumed",
        digits=(14, 5),
        compute="_compute_qty_consumed")

    @api.multi
    def _compute_qty_on_hand(self):
        for rec in self:
            products = self.env['stock.quant'].search(
                [('product_id', '=', rec.product_id.id),
                 ('location_id', '=',
                    rec.task_resource_id.project_id.location_id.id)])
            if products:
                for product in products:
                    rec.qty_on_hand += product.qty
            else:
                rec.qty_on_hand = 0

    @api.multi
    def _compute_qty_consumed(self):
        for rec in self:
            products = self.env['stock.move'].search(
                [('product_id', '=', rec.product_id.id),
                 ('product_id.type', '!=', 'service'),
                 ('location_id', '=',
                    rec.task_resource_id.project_id.location_id.id),
                 ('location_dest_id', '=',
                    rec.task_resource_id.project_id.
                    picking_out_id.default_location_dest_id.id),
                 ('state', '=', 'done')])

            services = self.env['account.invoice.line'].search(
                [('account_analytic_id', '=', rec.account_id.id),
                 ('product_id', '=', rec.product_id.id),
                 ('product_id.type', '=', 'service'),
                 ('invoice_id.state', 'in', ['open', 'paid'])])
            if products:
                for product in products:
                    rec.qty_consumed += product.product_uom_qty
            elif services:
                for service in services:
                    rec.qty_consumed += service.quantity
            else:
                rec.qty_consumed = 0
