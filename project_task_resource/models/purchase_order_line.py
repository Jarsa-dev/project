# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_project_insume = fields.Boolean(
        string='Is Project Insume',
        readonly=True, )
    specifications = fields.Char()

    @api.multi
    @api.constrains('product_qty')
    def _check_pr_qty(self):
        for rec in self:
            for line in rec.purchase_request_lines:
                if rec.product_qty > line.product_qty:
                    raise ValidationError(
                        _('The quantity must be lower than the quantity of'
                            ' the purchase request line. \n\n'
                            'Product: %s') % rec.product_id.name)
                if line.remaining_qty < 0.0:
                    raise ValidationError(
                        _('The quantity must be lower than the remaining '
                            'quantity of the purchase request line. \n\n'
                            'Product: %s') % rec.product_id.name)

    @api.multi
    def _create_stock_moves(self, picking):
        moves = super(PurchaseOrderLine, self)._create_stock_moves(picking)
        for rec in self:
            if rec.account_analytic_id:
                for move in moves:
                    move.account_analytic_id = rec.account_analytic_id.id
                    move.project_id = rec.env['project.task'].search(
                        [(
                            'analytic_account_id', '=',
                            rec.account_analytic_id.id)]).project_id.id
                    move.task_id = rec.env['project.task'].search(
                        [(
                            'analytic_account_id', '=',
                            rec.account_analytic_id.id)]).id
        return moves
