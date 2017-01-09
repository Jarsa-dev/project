# -*- coding: utf-8 -*-
# © 2013 Julius Network Solutions
# © 2015 Clear Corp
# © 2016 Andhitia Rama <andhitia.r@gmail.com>
# © 2017 Jarsa Sistemas S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    account_analytic_id = fields.Many2one(
        string='Analytic Account',
        comodel_name='account.analytic.account',
        )


class StockQuant(models.Model):

    _inherit = "stock.quant"

    @api.model
    def _prepare_account_move_line(self, move, qty, cost,
                                   credit_account_id, debit_account_id,
                                   context=None):
        res = super(StockQuant,
                    self)._prepare_account_move_line(
                        move, qty, cost,
                        credit_account_id,
                        debit_account_id,
                        context=context
                        )
        # Add analytic account in debit line
        if len(res) == 0:
            raise exceptions.ValidationError(
                _('Something was wrong creating the account'
                    ' move, please check the product and the'
                    ' location configurations.'))
        if move.account_analytic_id:
            res[0][2].update({
                'analytic_account_id': move.account_analytic_id.id,
            })
            res[1][2].update({
                'analytic_account_id': move.account_analytic_id.id,
            })
        return res
