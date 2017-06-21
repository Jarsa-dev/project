# -*- coding: utf-8 -*-0
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResourceControl(models.TransientModel):

    _inherit = 'resource.control.wizard'
    _name = 'resource.control.wizard'

    @api.multi
    def make_control(self):
        res = super(ResourceControl, self).make_control()
        res_control = self.env["resource.control"].search(
            [('id', '=', res['res_id'])])
        billing_requests = self.env['analytic.billing.plan'].search(
            [(
                'account_analytic_id',
                '=',
                res_control.task_id.analytic_account_id.id)])
        qty_requested = 0.0
        for request in billing_requests:
            qty_requested += request.quantity
            request.has_active_order = True

        res_control.task_id.remaining_quantity = 0.0
        res_control.task_id.write({'remaining_quantity': (
            res_control.task_id.real_qty - qty_requested)})

        return res
