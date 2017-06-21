# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    bridge_account_id = fields.Many2one(
        'account.account',
        string="Bridge Account",
        help="Account for the account moves generated "
        "by billing request confirmations",)
    billing_request_journal_id = fields.Many2one(
        'account.journal',
        string="Billing Request Journal",)
    product_id = fields.Many2one(
        'product.product',
        string='Product to Billing',
        domain=[('sale_ok', '=', True),
                ('type', '=', 'service')],
        )
