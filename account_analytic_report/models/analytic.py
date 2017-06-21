# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    parent_id = fields.Many2one(
        'account.analytic.account', string='Parent',
        index=True)
    child_parent_ids = fields.One2many(
        'account.analytic.account', 'parent_id', string='Children')
    child_id = fields.Many2many(
        'account.analytic.account', compute="_compute_get_child_ids",
        string="Child Accounts")
    analytic_debit = fields.Monetary(
        compute="_compute_analytic", string='Debit')
    analytic_credit = fields.Monetary(
        compute="_compute_analytic", string='Credit')
    analytic_balance = fields.Monetary(
        compute="_compute_analytic", string='Balance')

    @api.multi
    def _get_children(self, ids):
        ids = list(ids)
        res = []
        record = self.search([('parent_id', 'child_of', ids)])
        for rec in record:
            res.append(rec.id)
        return res

    @api.depends('child_parent_ids')
    def _compute_get_child_ids(self):
        for rec in self:
            result = []
            if rec.child_parent_ids:
                for record in rec.child_parent_ids:
                    result.append(record.id)
            rec.child_id = result

    def _compute_analytic(self):
        for rec in self:
            analytic_line_obj = rec.env['account.analytic.line']
            children_ids = rec._get_children(rec._ids)
            domain = [('account_id', 'in', (tuple(children_ids,)))]
            if rec._context.get('date_from', False):
                domain.append(('date', '>=', rec._context['date_from']))
            if rec._context.get('date_to', False):
                domain.append(('date', '<=', rec._context['date_to']))

            account_amounts = analytic_line_obj.search_read(
                domain, ['account_id', 'amount'])
            debit = 0.0
            credit = 0.0
            for account_amount in account_amounts:
                if account_amount['amount'] < 0.0:
                    credit += abs(account_amount['amount'])
                else:
                    debit += account_amount['amount']
            rec.analytic_debit = debit
            rec.analytic_credit = credit
            rec.analytic_balance = debit - credit
