# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, exceptions, fields, models


class TaskResource(models.Model):
    _inherit = 'project.task'

    line_billing_ids = fields.One2many('analytic.billing.plan.line', 'task_id')
    nbr_billing = fields.Float(
        string="Billing Request",
        compute="_compute_nbr_billing")
    remaining_quantity = fields.Float(
        default=0.0,
        compute="_compute_remaining_quantity",
        store=True,)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id,)
    billing_task_total = fields.Float(
        string='Billing Total',
        compute='_compute_billing_task_total',)

    @api.multi
    def _compute_billing_task_total(self):
        for rec in self:
            if rec.line_billing_ids:
                for line in rec.line_billing_ids:
                    if (line.analytic_billing_plan_id.state == 'confirm' and
                            line.analytic_billing_plan_id.
                            invoice_id.state in ['open', 'paid']):
                        rec.billing_task_total += line.amount
            else:
                rec.billing_task_total = 0.0

    @api.depends('line_billing_ids')
    def _compute_nbr_billing(self):
        for record in self:
            record.nbr_billing = len(record.line_billing_ids.search(
                [('task_id', '=', record.id)]))

    @api.multi
    @api.depends('line_billing_ids')
    def _compute_remaining_quantity(self):
        for rec in self:
            billing_request_total = 0.0
            for line in rec.line_billing_ids:
                if line.analytic_billing_plan_id.state == 'confirm':
                    billing_request_total += line.quantity
            rec.remaining_quantity = rec.qty - billing_request_total

    @api.multi
    def action_button_draft(self):
        for rec in self:
            if rec.nbr_billing > 0.0:
                raise exceptions.ValidationError(
                    _("You can't reset the concept because"
                        " it already has a billing request."))
        return super(TaskResource, self).action_button_draft()

    @api.multi
    def request_billing_request(self):
        return {
            'name': 'Billing Request',
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id':  self.env.ref(
                    'analytic_billing_plan.'
                    'analytic_billing_plan_line_tree_view').id,
            'res_model': 'analytic.billing.plan.line',
            'domain': [(
                'account_analytic_id', '=', self.analytic_account_id.id)],
            'context': {'search_default_analytic_billing_plan_group_by': 1},
            'type': 'ir.actions.act_window',
        }
