# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnalyticBillingPlanLine(models.Model):
    _name = 'analytic.billing.plan.line'
    _description = "Analytic Billing Plan Line"

    name = fields.Char()
    has_active_order = fields.Boolean(
        string='Billing request',
        help="Indicates that this billing plan line "
        "contains at least one non-cancelled billing request.",
        default=True)
    quantity = fields.Float(
        digits=(15, 4),)
    price_unit = fields.Float(
        "Price Unit",
        readonly=True,
    )
    amount = fields.Float(
        string='Amount',
        help=('Calculated by multiplying the quantity '
              'and the price given in the Product\'s '
              'cost price. Always expressed in the '
              'company main currency.'),
    )
    account_id = fields.Many2one('account.account', 'Account', readonly=True, )
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        required=True)
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    task_id = fields.Many2one('project.task', string='Concept')
    ref = fields.Char()
    move_id = fields.Many2one('account.move', string='Account Move')
    analytic_billing_plan_id = fields.Many2one(
        'analytic.billing.plan',
        string="Analytic_billing_Plan",
        readonly=True,)
    invoice_id = fields.Many2one(
        'account.invoice',
        string="Invoice",
        related="analytic_billing_plan_id.invoice_id",
        readonly=True, )
