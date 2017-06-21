# -*- coding: utf-8 -*-
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_approve(self):
        res = super(PurchaseOrder, self).button_approve()
        rfq = self.name
        self.write({
            'origin': rfq,
            'name': self.env['ir.sequence'].next_by_code(
                'purchase.confirmed')
        })
        return res
