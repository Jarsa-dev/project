# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models


class WizardBillingPlan(models.TransientModel):
    _inherit = 'wizard.billing.plan'

    qty = fields.Float(string='Planned Quantity',)
    real_qty = fields.Float(string='Real Quantity')

    @api.model
    def _prepare_item(self, line):
        res = super(WizardBillingPlan, self)._prepare_item(line)
        res['real_qty'] = line.real_qty
        return res

    @api.multi
    def create_billing(self):
        for rec in self:
            res = super(WizardBillingPlan, self).create_billing()
            billing_request = self.env['analytic.billing.plan'].browse(
                res['res_id'])
            if billing_request:
                for line in billing_request.analytic_billing_plan_line_ids:
                    if line.task_id.real_qty == line.quantity:
                        line.ref = _(
                            "Total Billing of: Concept: %s - Quantity: %s" %
                            (line.task_id.description,
                                line.quantity,))
                        line.active_order = False
                    if line.quantity < line.task_id.real_qty:
                        line.ref = _(
                            "Partial Billing of: Concept: %s - Quantity: %s" %
                            (line.task_id.description,
                                line.quantity,))
                        line.active_order = True
            return res
