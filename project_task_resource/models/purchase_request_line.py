# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    product_qty = fields.Float(
        digits=(14, 4),
        string='Quantity',)
    qty_on_hand = fields.Float(
        string="Quantity on Hand",
        digits=(14, 4),
        compute="_compute_qty_on_hand",
    )
    is_project_insume = fields.Boolean(
        string='Is Project Insume?',)
    purchase_lines = fields.Many2many(
        'purchase.order.line', 'purchase_request_purchase_order_line_rel',
        'purchase_request_line_id',
        'purchase_order_line_id', 'Purchase Order Lines',
        readonly=True, copy=False)
    purchase_state = fields.Selection(
        store=True,
    )
    remaining_qty = fields.Float(
        string="Remaining Quantity",
        digits=(14, 4),
        compute="_compute_remaining_qty",
        default=0.0,
    )
    purchased_qty = fields.Float(
        digits=(14, 4),
    )

    @api.multi
    @api.depends('purchased_qty')
    def _compute_remaining_qty(self):
        for rec in self:
            if rec.purchased_qty > 0.0:
                rec.remaining_qty = rec.product_qty - rec.purchased_qty
            else:
                rec.remaining_qty = rec.product_qty

    @api.multi
    def _compute_qty_on_hand(self):
        for rec in self:
            products = self.env['stock.quant'].search(
                [('product_id', '=', rec.product_id.id),
                 ('location_id', '=',
                    rec.request_id.project_id.location_id.id)])
            if products:
                for product in products:
                    rec.qty_on_hand += product.qty
            else:
                rec.qty_on_hand = 0
