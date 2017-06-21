# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class WizardBillingPlanLine(models.TransientModel):
    _name = 'wizard.billing.plan.line'

    project_task = fields.Many2one('project.task', readonly=True)
    remaining_quantity = fields.Float(compute="_compute_remaining_quantity",)
    total_invoice = fields.Float(compute='_compute_total_invoice')
    quantity_invoice = fields.Float()
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    unit_price = fields.Float(readonly=True)
    qty = fields.Float(readonly=True)
    billing_request_id = fields.Many2one('wizard.billing.plan', string="BR")

    @api.depends('quantity_invoice', 'unit_price')
    def _compute_total_invoice(self):
        for rec in self:
            rec.total_invoice = rec.quantity_invoice * rec.unit_price

    @api.depends('qty', 'quantity_invoice')
    def _compute_remaining_quantity(self):
        for rec in self:
            rec.remaining_quantity = rec.qty - rec.quantity_invoice
