# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseRequestLine(models.TransientModel):

    _name = 'purchase.request.line.wizard'
    _description = 'Wizard of purchase request'

    wiz_id = fields.Many2one('purchase.request.wizard')
    line_id = fields.Many2one(
        'analytic.resource.plan.line',
        string='Resource Line',
        required=True,
        readonly=True,)
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        related='line_id.account_id',
        string='Analytic Account',
        readonly=True,)
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        readonly=True,)
    uom_id = fields.Many2one('product.uom', string='UoM', readonly=True,)
    qty = fields.Float(
        string='Quantity Planned',
        readonly=True,
        digits=(14, 4),
        )
    real_qty = fields.Float(
        string="Real Quantity",
        readonly=True,
        digits=(14, 4),
        )
    qty_on_hand = fields.Float(
        string='Quantity On Hand',
        readonly=True,
        digits=(14, 4),
        )
    qty_to_request = fields.Float(
        string="Quantity To Request",
        digits=(14, 4),
        )
    requested_qty = fields.Float(
        readonly=True,
        digits=(14, 4),
        )
