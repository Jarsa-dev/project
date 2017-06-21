# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class WizardBillingPlanLine(models.TransientModel):
    _inherit = 'wizard.billing.plan.line'

    qty = fields.Float(
        string='Planned Quantity',
        readonly=True,)
    real_qty = fields.Float(
        string='Real Quantity',
        readonly=True,)

    @api.depends('qty', 'quantity_invoice')
    def _compute_remaining_quantity(self):
        for rec in self:
            rec.remaining_quantity = rec.real_qty - rec.quantity_invoice
